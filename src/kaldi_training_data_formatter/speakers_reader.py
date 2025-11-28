import os.path
from typing import Final

from kaldi_training_data_formatter import AbstractFileReader, Speaker, SPEAKERS_FILENAME


class SpeakersReader(AbstractFileReader):
    __COMMENT: Final[str] = ';'

    def __init__(self, filepath: str):
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, SPEAKERS_FILENAME)

        super().__init__(filepath, encoding='utf-8-sig', is_file=True)

    def read_all_speakers(self) -> list[Speaker]:
        speakers: list[Speaker] = []
        speaker: Speaker

        while speaker := self.read_speaker():
            speakers.append(speaker)

        return speakers

    def read_speaker(self) -> Speaker | None:
        line: str

        while line := self._read_line():
            if not line.startswith(SpeakersReader.__COMMENT):
                return Speaker.from_line(line)

        return None
