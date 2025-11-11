import os
import unittest

from case.file_test_case import FileTestCase
from kaldi_training_data_formatter import VocabCompiler


class TestVocabCompiler(FileTestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources_path: str = os.path.join(os.getcwd(), 'resources')
        cls.input_path: str = os.path.join(cls.resources_path, 'input')
        cls.output_path: str = os.path.join(cls.resources_path, 'output')

    def setUp(self):
        self.class_under_test: VocabCompiler = VocabCompiler(self.__class__.input_path, self.__class__.output_path)

    def read_vocabulary_given_valid_input_file_has_expected_vocabulary(self):
        # Arrange
        expected: set[str] = {
            'a',
            'all',
            'and',
            'as',
            'aspire',
            'been',
            'brighter',
            'chance',
            'chasing',
            'desire',
            'dreamer',
            'ever',
            'fire',
            'have',
            'higher',
            'i',
            'light',
            'lighter',
            'like',
            'my',
            'never',
            'out',
            'sinner',
            'spreading',
            'start',
            'take',
            'that',
            'the',
            'we',
            'wildfire',
            'with',
            'you',
        }

        # Act
        self.class_under_test.read_vocabulary()

        # Assert
        self.assertSetEqual(expected, self.class_under_test.vocabulary)

    def test_save_vocabulary_given_valid_input_file_creates_expected_output_file(self):
        # Arrange
        expected_path: str = os.path.join(self.__class__.resources_path, 'expected-vocab.txt')
        actual_path: str = os.path.join(self.__class__.output_path, VocabCompiler.VOCAB_FILENAME)

        # Assumptions
        self.assertFileExists(expected_path,
                              'assume that vocab file with expected data exists')

        # Arrange (cont.)
        self.class_under_test.read_vocabulary()

        # Act
        self.class_under_test.save_vocabulary()

        # Assert
        self.assertFileExists(actual_path,
                              'Assert that vocab file exists')
        self.assertFileEqual(open(expected_path, mode='r', encoding='utf-8-sig'),
                             open(actual_path, mode='r', encoding='utf-8-sig'),
                             'Assert that vocab in actual file equals expected file')


if __name__ == '__main__':
    unittest.main()
