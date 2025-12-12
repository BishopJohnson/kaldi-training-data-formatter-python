import copy
import os.path
import shutil
from typing import Final

from kaldi_training_data_formatter import \
    AUDIO_DIR_NAME, \
    SPEAKERS_FILENAME, \
    FilesUtil, \
    ProjectUtil, \
    Speaker, \
    SpeakersReader, \
    SpeakersWriter


class SpeakersSplitter:
    def __init__(self, input_root: str, output_root: str):
        self.__input_root: Final[str] = input_root
        self.__output_root: Final[str] = output_root
        self.__max_chapters_per_speaker: int = 0
        self.__verbose: bool = False

    @property
    def max_chapters_per_speaker(self) -> int:
        return self.__max_chapters_per_speaker

    @max_chapters_per_speaker.setter
    def max_chapters_per_speaker(self, value: int) -> None:
        self.__max_chapters_per_speaker = value

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self.__verbose = value

    @classmethod
    def from_root(cls, root: str):
        return cls(root, root)

    def split(self, is_sorted: bool = True) -> None:
        if self.max_chapters_per_speaker < 1:
            if self.verbose:
                print('Skipping splitting speakers: max_chapters_per_speaker is less than 1')
            return

        speakers_filepath: str = os.path.join(self.__input_root, SPEAKERS_FILENAME)
        speakers: list[Speaker] = []
        reserved_speaker_ids: set[int] = set()

        with SpeakersReader(speakers_filepath) as reader:
            while speaker := reader.read_speaker():
                if speaker.speaker_id in reserved_speaker_ids:
                    raise Exception(f'Detected duplicate speaker ID "{speaker.speaker_id}" when splitting speakers')

                speakers.append(speaker)
                reserved_speaker_ids.add(speaker.speaker_id)

        input_audio_path: str = os.path.join(self.__input_root, AUDIO_DIR_NAME)
        output_audio_path: str = os.path.join(self.__output_root, AUDIO_DIR_NAME)
        new_speakers: list[Speaker] = []
        updated_speakers: bool = False
        next_id: int = 1

        for speaker in speakers:
            new_speakers.append(speaker)

            # Get the chapters associated with the speaker
            speaker_path: str = os.path.join(input_audio_path,
                                             str(speaker.speaker_id),
                                             speaker.subset if is_sorted else '')
            transcript_paths: list[str] = FilesUtil.get_transcript_file_paths(speaker_path)
            alt_speaker_count: int = 0

            # Split chapters until below threshold
            while len(transcript_paths) > self.max_chapters_per_speaker:
                new_speaker: Speaker = copy.copy(speaker)

                # Count until the next available speaker ID is reached
                while next_id in reserved_speaker_ids:
                    next_id += 1

                # Update properties for the new speaker
                new_speaker.speaker_id = next_id
                new_speaker.name = f'{speaker.name} (alt {alt_speaker_count + 1} for utterance)'
                next_id += 1
                alt_speaker_count += 1

                # Create output directory for new speaker
                new_speaker_path: str = os.path.join(output_audio_path,
                                                     str(new_speaker.speaker_id),
                                                     new_speaker.subset if is_sorted else '')
                os.makedirs(new_speaker_path, exist_ok=True)

                # Move maximum amount of chapters to output path for the new speaker
                split_idx: int = len(transcript_paths) - self.max_chapters_per_speaker
                new_speaker_transcripts: list[str] = transcript_paths[split_idx:]
                transcript_paths = transcript_paths[:split_idx]

                for transcript_path in new_speaker_transcripts:
                    _, song_id = ProjectUtil.get_user_and_project_id(transcript_path)
                    src_path: str = os.path.join(speaker_path, song_id)

                    shutil.move(src_path, new_speaker_path)

                    if self.verbose:
                        print(f'Split off chapter from "{src_path}" to "{new_speaker_path}"')

                # Add the new speaker to the collections
                new_speakers.append(new_speaker)
                reserved_speaker_ids.add(new_speaker.speaker_id)
                updated_speakers = True

            # Move leftover chapters to output path
            output_speaker_path: str = os.path.join(output_audio_path,
                                                    str(speaker.speaker_id),
                                                    speaker.subset if is_sorted else '')

            if not speaker_path == output_speaker_path:
                os.makedirs(output_speaker_path, exist_ok=True)
                shutil.move(speaker_path, output_speaker_path)

        if updated_speakers:
            new_speakers.sort()
            SpeakersWriter().write_speakers(self.__output_root, new_speakers)
