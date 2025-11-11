import os.path
import unittest

from src.kaldi_training_data_formatter import TranscriptReader, TranscriptLine


class TestTranscriptReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources_path: str = os.path.join(os.getcwd(), 'resources/input')

    def test_read_transcript_line(self):
        param_list = [
            # transcript_name, expected
            ('test-transcript.trans.txt', [
                TranscriptLine.from_line('[0000] fire fire light the fire'),
                TranscriptLine.from_line('[0001] brighter higher as you desire'),
                TranscriptLine.from_line('[0002] chasing all that we aspire'),
                TranscriptLine.from_line('[0003] spreading out like wildfire'),
                TranscriptLine.from_line('[0004] never ever have i ever'),
                TranscriptLine.from_line('[0005] been a sinner been a dreamer'),
                TranscriptLine.from_line('[0006] take the chance and with my lighter'),
                TranscriptLine.from_line('[0007] start the fire'),
            ])
        ]

        for transcript_name, expected in param_list:
            with self.subTest():
                # Arrange
                path: str = TestTranscriptReader.__create_path(transcript_name)

                with TranscriptReader(path) as class_under_test:
                    # Act
                    actual: list[TranscriptLine] = class_under_test.read_all_lines()

                    # Assert
                    self.assertListEqual(expected, actual)

    @classmethod
    def __create_path(cls, filename: str) -> str:
        return os.path.join(cls.resources_path, filename)


if __name__ == '__main__':
    unittest.main()
