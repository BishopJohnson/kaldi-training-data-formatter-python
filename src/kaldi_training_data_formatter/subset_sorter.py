import os.path
import random
import shutil
from enum import Enum
from typing import Final

from kaldi_training_data_formatter import Speaker, SpeakersReader, SpeakersWriter, AUDIO_DIR_NAME


class SubsetSorter:
    class Builder:
        def __init__(self):
            self.__input_root: str | None = None
            self.__output_root: str | None = None
            self.__test_subset_speakers: set[int] = set()
            self.__train_subset_speakers: set[int] = set()

        def add_test_subset_speaker(self, speaker_id: int):
            self.__test_subset_speakers.add(speaker_id)
            return self

        def add_train_subset_speaker(self, speaker_id: int):
            self.__train_subset_speakers.add(speaker_id)
            return self

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

    class __SubsetType(Enum):
        Train = 0
        Test = 1

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

    def sort_sources(self) -> None:
        # Shuffle unsorted speakers and assign them to subsets
        random.shuffle(self.__unsorted_speakers)

        for speaker in self.__unsorted_speakers:
            # TODO: Randomize between train and test with a given ratio of training to testing data
            speaker.subset = self.__train_dir_name
            self.__sorted_speakers.append(speaker)

        # Reorder sorted speakers by ID
        self.__sorted_speakers.sort()

        # Move data to assigned subsets
        for speaker in self.__sorted_speakers:
            speaker_id: str = str(speaker.speaker_id)
            unsorted_input_path: str = os.path.join(self.__input_root, AUDIO_DIR_NAME, speaker_id)
            sorted_input_path: str = os.path.join(self.__input_root, AUDIO_DIR_NAME, speaker.subset, speaker_id)
            sorted_output_path: str = os.path.join(self.__output_root, AUDIO_DIR_NAME, speaker.subset, speaker_id)

            # Move data to output directory and remove input directory
            os.makedirs(sorted_output_path, exist_ok=True)

            if os.path.isdir(unsorted_input_path):
                shutil.move(unsorted_input_path, sorted_output_path)

                if not unsorted_input_path == sorted_output_path:
                    shutil.rmtree(unsorted_input_path)
            elif os.path.isdir(sorted_input_path):
                shutil.move(sorted_input_path, sorted_output_path)

                if not sorted_input_path == sorted_output_path:
                    shutil.rmtree(sorted_input_path)
            else:
                raise Exception(f'No input data for speaker {speaker.speaker_id}')

        # Writer new speakers file
        SpeakersWriter().write_speakers(self.__output_root, self.__sorted_speakers)

    @staticmethod
    def builder() -> Builder:
        return SubsetSorter.Builder()
