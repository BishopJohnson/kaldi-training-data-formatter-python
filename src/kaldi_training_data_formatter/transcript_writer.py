import os.path
from typing import Final, Collection

from kaldi_training_data_formatter import TranscriptLine


class TranscriptWriter:
    __EXTENSION: Final[str] = '.trans.txt'

    def __init__(self, root: str):
        self.__root: Final[str] = root

    def write_transcript(self, filename: str, lines: Collection[TranscriptLine] | Collection[str]) -> None:
        if not filename.endswith(TranscriptWriter.__EXTENSION):
            filename += TranscriptWriter.__EXTENSION

        filepath: str = os.path.join(self.__root, filename)
        directory: str = os.path.dirname(filepath)

        if not os.path.isdir(directory):
            raise Exception(f'Directory does not exist: "{directory}"')

        try:
            os.makedirs(directory, exist_ok=True)

            with open(filepath, mode='w', encoding='utf-8') as f:
                text_lines: Collection[str] = lines if type(lines) is Collection[str] else [
                    str(line)
                    for line in lines
                ]

                for line in text_lines:
                    f.write(line)
                    f.write('\n')
        except Exception as e:
            print('Error while writing transcript file: ' + str(e))
