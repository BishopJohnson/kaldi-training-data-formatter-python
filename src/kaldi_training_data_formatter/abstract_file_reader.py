import os.path
from abc import ABC
from io import TextIOWrapper


class AbstractFileReader(ABC):
    def __init__(self, path: str, encoding: str, is_file: bool = True):
        # Init fields
        self.__encoding = encoding
        self.__file: TextIOWrapper | None = None
        self.__is_closed: bool = False

        # Init property values
        self.__current_line = 0

        if is_file:
            if not os.path.isfile(path):
                raise Exception(f'path is not a file: "{path}"')

            self.__filepath = path
            self.__filename = os.path.basename(path)
            self.__directory = os.path.dirname(path)
        else:
            if not os.path.isdir(path):
                raise Exception(f'path is not a directory: "{path}"')

            self.__directory = path
            self.__filepath = None
            self.__filename = None

    @property
    def directory(self) -> str:
        return self.__directory

    @property
    def _current_line(self) -> int:
        return self.__current_line

    @property
    def _filename(self) -> str:
        return self.__filename

    @property
    def _filepath(self) -> str:
        return self.__filepath

    def _read_line(self) -> str | None:
        line: str = self.__file.readline()

        # Checks for no text (blank lines will still have new-line character)
        if not line:
            return None

        self.__current_line += 1

        return line.strip('\n\r ')

    def __enter__(self):
        self.__file = open(self._filepath, mode='r', encoding=self.__encoding)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__is_closed:
            return

        if self.__file is not None:
            self.__file.close()
            self.__file = None
