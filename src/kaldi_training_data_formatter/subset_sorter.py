import os.path
import random
import shutil
from typing import Final

from kaldi_training_data_formatter import Speaker, SpeakersReader, SpeakersWriter, AUDIO_DIR_NAME


class SubsetSorter:
    class Builder:
        def __init__(self):
            self.__input_root: str | None = None
            self.__output_root: str | None = None
            self.__test_speakers: float | None

        def build(self):
            if self.__input_root is None:
                raise Exception('')

            if self.__output_root is None:
                raise Exception('')

            return SubsetSorter(input_root=self.__input_root,
                                output_root=self.__output_root,
                                train_dir_name='train-clean',
                                test_dir_name='test-clean')

        def set_input_root(self, value: str):
            self.__input_root = value
            return self

        def set_output_root(self, value: str):
            self.__output_root = value
            return self

    def __init__(self,
                 input_root: str,
                 output_root: str,
                 train_dir_name: str,
                 test_dir_name: str):
        self.__input_root: Final[str] = input_root
        self.__output_root: Final[str] = output_root
        self.__train_dir_name: Final[str] = train_dir_name
        self.__test_dir_name: Final[str] = test_dir_name
        self.__sorted_speakers: Final[list[Speaker]] = []
        self.__unsorted_speakers: Final[list[Speaker]] = []

    def gather_sources(self) -> None:
        self.__sorted_speakers.clear()
        self.__unsorted_speakers.clear()

        if not os.path.isdir(self.__input_root):
            raise Exception(f'Input root is not a directory: "{self.__input_root}"')

        with SpeakersReader(self.__input_root) as reader:
            subset_names: list[str] = [self.__train_dir_name, self.__test_dir_name]
            speaker: Speaker

            while speaker := reader.read_speaker():
                # Check if speaker was already assigned a valid subset
                if speaker.subset in subset_names:
                    self.__sorted_speakers.append(speaker)
                else:
                    self.__unsorted_speakers.append(speaker)

    def sort_sources(self, test_speakers: float = 0.0) -> None:
        # Determine how many speakers to put in test subset
        test_speakers_count: int = sum(1 for el in self.__sorted_speakers if el.subset == self.__test_dir_name)
        target_num_of_test_speakers: int

        if test_speakers >= 1.0 and test_speakers.is_integer():
            target_num_of_test_speakers = int(test_speakers)
        elif 0.0 <= test_speakers < 1.0:
            speakers_count: int = len(self.__unsorted_speakers) + len(self.__sorted_speakers)
            target_num_of_test_speakers = round(speakers_count * test_speakers)
        else:
            raise Exception('Value for test_speakers must either be a non-negative integer or a value between (0, 1)')

        # Shuffle unsorted speakers and assign them to subsets
        random.shuffle(self.__unsorted_speakers)

        for speaker in self.__unsorted_speakers:
            if test_speakers_count < target_num_of_test_speakers:
                speaker.subset = self.__test_dir_name
                test_speakers_count += 1
            else:
                speaker.subset = self.__train_dir_name

            self.__sorted_speakers.append(speaker)

        # Reorder sorted speakers by ID
        self.__sorted_speakers.sort()

        # Move data to assigned subsets
        for speaker in self.__sorted_speakers:
            speaker_id: str = str(speaker.speaker_id)
            unsorted_input_path: str = os.path.join(self.__input_root, AUDIO_DIR_NAME, speaker_id)
            sorted_input_path: str = os.path.join(self.__input_root, AUDIO_DIR_NAME, speaker.subset, speaker_id)
            sorted_output_path: str = os.path.join(self.__output_root, AUDIO_DIR_NAME, speaker.subset)

            # Move data to output directory and remove input directory
            os.makedirs(sorted_output_path, exist_ok=True)

            if os.path.isdir(unsorted_input_path):
                shutil.move(unsorted_input_path, sorted_output_path)
            elif os.path.isdir(sorted_input_path):
                shutil.move(sorted_input_path, sorted_output_path)
            else:
                raise Exception(f'No input data for speaker {speaker.speaker_id}')

        # Writer new speakers file
        SpeakersWriter().write_speakers(self.__output_root, self.__sorted_speakers)

    @staticmethod
    def builder() -> Builder:
        return SubsetSorter.Builder()
