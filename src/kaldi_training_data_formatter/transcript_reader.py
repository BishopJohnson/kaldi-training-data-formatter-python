from kaldi_training_data_formatter import AbstractFileReader, TranscriptLine


class TranscriptReader(AbstractFileReader):
    def __init__(self, filepath: str):
        super().__init__(filepath, encoding='utf-8-sig', is_file=True)

    def read_all_lines(self) -> list[TranscriptLine]:
        lines: list[TranscriptLine] = []
        line: TranscriptLine

        while line := self.read_transcript_line():
            lines.append(line)

        return lines

    def read_transcript_line(self) -> TranscriptLine | None:
        line: str

        # Loop until a line with some data is encountered
        while not (line := self._read_line()):
            # End once end of file is reached
            if line is None:
                return None

        try:
            return TranscriptLine.from_line(line)
        except Exception as e:
            raise e
