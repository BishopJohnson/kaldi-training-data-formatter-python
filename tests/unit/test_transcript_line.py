import unittest
from typing import Tuple

from src.kaldi_training_data_formatter import TranscriptLine


class TestTranscriptLine(unittest.TestCase):
    def test_eq_when_other_is_none_returns_false(self):
        param_list: list[str] = [
            # line
            '0',
            '0 hello world',
        ]

        for line in param_list:
            with self.subTest():
                # Arrange
                class_under_test: TranscriptLine = TranscriptLine.from_line(line)
                other: None = None

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertFalse(actual)

    def test_eq_when_other_is_same_returns_true(self):
        param_list: list[str] = [
            # line
            '0',
            '0 hello world',
        ]

        for line in param_list:
            with self.subTest():
                # Arrange
                class_under_test: TranscriptLine = TranscriptLine.from_line(line)
                other: TranscriptLine = class_under_test

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertTrue(actual)

    def test_eq_when_other_does_not_have_same_properties_returns_false(self):
        param_list: list[Tuple[str, str]] = [
            # line, (other_)line
            ('0', '1'),
            ('0 hello world', '1 fire fire light the fire'),
        ]

        for line, other_line in param_list:
            with self.subTest():
                # Arrange
                class_under_test: TranscriptLine = TranscriptLine.from_line(line)
                other: TranscriptLine = TranscriptLine.from_line(other_line)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertFalse(actual)

    def test_eq_when_other_does_have_same_properties_returns_true(self):
        param_list: list[str] = [
            # line
            '0',
            '0 hello world',
        ]

        for line in param_list:
            with self.subTest():
                # Arrange
                class_under_test: TranscriptLine = TranscriptLine.from_line(line)
                other: TranscriptLine = TranscriptLine.from_line(line)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertTrue(actual)

    def test_from_line_given_empty_line_raises_exception(self):
        # Arrange
        expected = Exception
        line: str = ''

        # Assert
        with self.assertRaises(expected):
            TranscriptLine.from_line(line)

    def test_from_line_given_valid_line_returns_expected(self):
        param_list: list[Tuple[str, str, list[str]]] = [
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
        param_list: list[Tuple[str, list[str], str]] = [
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
