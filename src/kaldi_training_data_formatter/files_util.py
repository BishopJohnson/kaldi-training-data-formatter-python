import os.path
from enum import Enum
from typing import Final, Tuple

from src.kaldi_training_data_formatter import TranscriptLine, TranscriptReader, ProjectUtil


class FilesUtil:
    __EXTENSION: Final[str] = '.trans.txt'

    class __FormatType(Enum):
        Audio = 0
        Transcript = 1

    @staticmethod
    def format_audio_files(root: str) -> None:
        FilesUtil.__format_files(root, FilesUtil.__FormatType.Audio)

    @staticmethod
    def __format_audio_files_for_transcript(transcript_path: str) -> None:
        directory: str = os.path.dirname(transcript_path)
        print(directory)

        if not directory:
            print("Transcript directory is not valid")
            return

        user_id, project_id = ProjectUtil.get_user_and_project_id(directory)
        print('; '.join([user_id, project_id]))

        # lines: dict[str, TranscriptLine] = FilesUtil.__get_transcript_lines(transcript_path)

    @staticmethod
    def __format_files(root: str, format_type: __FormatType) -> None:
        if not os.path.isdir(root):
            return

        directories_queue = [root]

        while len(directories_queue) > 0:
            directory = directories_queue.pop()
            directories_queue += [f.path for f in os.scandir(directory) if f.is_dir()]

            (has_transcript, transcript_path) = FilesUtil.__has_transcript_file(directory)

            if not has_transcript:
                continue

            match format_type:
                case FilesUtil.__FormatType.Audio:
                    break

                case FilesUtil.__FormatType.Transcript:
                    break

                case _:
                    raise Exception(f'Invalid format type {format_type}')

    @staticmethod
    def __get_transcript_lines(transcript_path: str) -> dict[str, TranscriptLine]:
        lines = {}

        with TranscriptReader(transcript_path) as reader:
            line: TranscriptLine

            while line := reader.read_transcript_line():
                if line.id in lines.keys():
                    pass  # TODO: Handle duplicate IDs.
                else:
                    lines[line.id] = line

        return lines

    @staticmethod
    def __has_transcript_file(directory: str) -> Tuple[bool, str | None]:
        files: list[str] = [
            f.path
            for f in os.scandir(directory)
            if f.is_file() and f.path.endswith(FilesUtil.__EXTENSION)
        ]

        if len(files) > 0:
            return True, files[0]
        else:
            return False, None
