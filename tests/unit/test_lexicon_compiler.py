import os
import unittest

from case.file_test_case import FileTestCase
from kaldi_training_data_formatter import LexiconCompiler


class TestLexiconCompiler(FileTestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources_path: str = os.path.join(os.getcwd(), 'resources')
        cls.input_path: str = os.path.join(cls.resources_path, 'input')
        cls.output_path: str = os.path.join(cls.resources_path, 'output')

    def test_compile_lexicon_when_import_lexicon_has_entry_with_no_phones_skips_entry(self):
        # Arrange
        vocabulary: list[str] = [
            'a',
        ]
        class_under_test: LexiconCompiler = LexiconCompiler(self.__class__.input_path, self.__class__.output_path)
        class_under_test.set_import_lexicon('test-import-lexicon-no-phones.txt')

        # Act
        class_under_test.compile_lexicon(vocabulary, use_existing=False)

        # Assert
        with self.subTest():
            for vocab in vocabulary:
                self.assertTrue(vocab in class_under_test.lexicon.keys(),
                                'Assert that vocabulary is in lexicon')
                self.assertTrue(len(class_under_test.lexicon[vocab]) == 0,
                                'Assert that vocabulary has no phones')

    def test_save_lexicon_when_all_vocabulary_has_phones_creates_expected_output_file(self):
        param_list: list[tuple[str, list[str], str]] = [
            # lexicon, vocabulary, expected
            ('test-import-lexicon.txt', [
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
            ], 'expected-lexicon-1.txt'),
        ]

        for lexicon, vocabulary, expected in param_list:
            with self.subTest():
                # Arrange
                expected_path: str = os.path.join(self.__class__.resources_path, expected)
                actual_path: str = os.path.join(self.__class__.output_path, LexiconCompiler.LEXICON_FILENAME)
                import_path: str = os.path.join(self.__class__.input_path, lexicon)

                # Assumptions
                self.assertFileExists(expected_path,
                                      'Assume that lexicon file with expected data exists')
                self.assertFileExists(import_path,
                                      'Assume that lexicon file with import data exists')

                # Arrange (cont.)
                class_under_test: LexiconCompiler = LexiconCompiler(self.__class__.input_path,
                                                                    self.__class__.output_path)
                class_under_test.set_import_lexicon(lexicon)
                class_under_test.compile_lexicon(vocabulary, use_existing=False)

                # Act
                class_under_test.save_lexicon()

                # Assert
                self.assertFileExists(actual_path,
                                      'Assert that lexicon file exists')
                self.assertFileEqual(open(expected_path, mode='r', encoding='utf-8-sig'),
                                     open(actual_path, mode='r', encoding='utf-8-sig'),
                                     'Assert that lexicon in actual file equals expected file')

    def test_save_lexicon_when_vocabulary_has_no_phones_creates_expected_output_file(self):
        param_list: list[tuple[list[str], str]] = [
            # vocabulary, expected
            ([
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
             ], 'expected-lexicon-2.txt'),
        ]

        for vocabulary, expected in param_list:
            with self.subTest():
                # Arrange
                expected_path: str = os.path.join(self.__class__.resources_path, expected)
                actual_path: str = os.path.join(self.__class__.output_path, LexiconCompiler.LEXICON_FILENAME)

                # Assumptions
                self.assertFileExists(expected_path,
                                      'Assume that lexicon file with expected data exists')

                # Arrange (cont.)
                class_under_test: LexiconCompiler = LexiconCompiler(self.__class__.input_path,
                                                                    self.__class__.output_path)
                class_under_test.compile_lexicon(vocabulary, use_existing=False)

                # Act
                class_under_test.save_lexicon()

                # Assert
                self.assertFileExists(actual_path,
                                      'Assert that lexicon file exists')
                self.assertFileEqual(open(expected_path, mode='r', encoding='utf-8-sig'),
                                     open(actual_path, mode='r', encoding='utf-8-sig'),
                                     'Assert that lexicon in actual file equals expected file')

    def test_save_lexicon_when_using_multiple_import_lexicons_creates_expected_output_file(self):
        param_list: list[tuple[list[str], list[str], str]] = [
            # lexicons, vocabulary, expected
            (['test-import-lexicon-A.txt', 'test-import-lexicon-B.txt'], [
                'brighter',
                'fire',
            ], 'expected-lexicon-AB.txt'),
        ]

        for lexicons, vocabulary, expected in param_list:
            with self.subTest():
                # Arrange
                expected_path: str = os.path.join(self.__class__.resources_path, expected)
                actual_path: str = os.path.join(self.__class__.output_path, LexiconCompiler.LEXICON_FILENAME)

                # Assumptions
                self.assertFileExists(expected_path,
                                      'Assume that lexicon file with expected data exists')

                # Arrange (cont.)
                class_under_test: LexiconCompiler = LexiconCompiler(self.__class__.input_path,
                                                                    self.__class__.output_path)
                class_under_test.set_import_lexicons(lexicons)
                class_under_test.compile_lexicon(vocabulary, use_existing=False)

                # Act
                class_under_test.save_lexicon()

                # Assert
                self.assertFileExists(actual_path,
                                      'Assert that lexicon file exists')
                self.assertFileEqual(open(expected_path, mode='r', encoding='utf-8-sig'),
                                     open(actual_path, mode='r', encoding='utf-8-sig'),
                                     'Assert that lexicon in actual file equals expected file')


if __name__ == '__main__':
    unittest.main()
