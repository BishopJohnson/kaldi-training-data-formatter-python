import unittest
from src.kaldi_training_data_formatter import TranscriptLine


class TestTranscriptLine(unittest.TestCase):
    def test_from_line_given_empty_line_raises_exception(self):
        # Arrange
        expected = Exception
        line: str = ''

        # Assert
        with self.assertRaises(expected):
            TranscriptLine.from_line(line)

    def test_from_line_given_valid_line_returns_expected(self):
        param_list = [
            # line, (expected_)id, (expected_)text
            ('0', '0', []),
            ('0 hello world', '0', ['hello', 'world']),
            ('  0 hello world  \n', '0', ['hello', 'world']),
        ]

        for line, expected_id, expected_text in param_list:
            with self.subTest():
                # Act
                actual = TranscriptLine.from_line(line)

                # Assert
                with self.subTest():
                    self.assertEqual(expected_id, actual.id, 'Actual ID does not equal expected')
                with self.subTest():
                    self.assertListEqual(expected_text, actual.text, 'Actual text does not equal expected')

    def test_str_returns_expected(self):
        param_list = [
            # (line_)id, text, expected
            ('0', ['hello', 'world'], '0 hello world'),
        ]

        for line_id, text, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test = TranscriptLine(line_id, text)

                # Act
                actual = str(class_under_test)

                # Assert
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
