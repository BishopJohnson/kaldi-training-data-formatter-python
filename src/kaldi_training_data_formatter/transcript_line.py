from typing import Tuple


class TranscriptLine:
    def __init__(self, line_id: str, text: list[str]):
        self.__id: str = line_id
        self.__text: list[str] = text

    @classmethod
    def from_line(cls, line: str):
        line_id, text = TranscriptLine.__parse_line(line)

        return cls(line_id, text)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def text(self) -> list[str]:
        return self.__text

    def __str__(self) -> str:
        str_list: list[str] = [self.id]
        str_list += self.text

        return ' '.join(str_list)

    @staticmethod
    def __parse_line(line: str) -> Tuple[str, list[str]]:
        data: list[str] = [
            s.strip('\n\r\t ')
            for s in line.split(' ')
            if s.strip()  # Not `None` or white-space
        ]

        if len(data) < 1:
            raise Exception('Line has no text')

        line_id: str = data[0]
        text: list[str] = data[1:]

        return line_id, text
