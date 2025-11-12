import unittest

from kaldi_training_data_formatter import Chapter


class TestChapter(unittest.TestCase):
    def test_str_returns_expected(self):
        param_list: list[tuple[int, int, str, int, str, str]] = [
            # (chapter_)id, project_id, song_id, speaker_id, subset, expected
            (1, 1, 'song', 1, 'subset', '1 | 1 | subset | 1 | song'),
            (100, 1, 'CVRD-438', 1, 'train-clean', '100 | 1 | train-clean | 1 | CVRD-438'),
        ]

        for chapter_id, project_id, song_id, speaker_id, subset, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(chapter_id)
                class_under_test.project_id = project_id
                class_under_test.song_id = song_id
                class_under_test.speaker_id = speaker_id
                class_under_test.subset = subset

                # Act
                actual: str = str(class_under_test)

                # Assert
                self.assertEqual(expected, actual)

    def test_ge_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = None

        # Act
        actual: bool = class_under_test >= other

        # Assert
        self.assertTrue(actual)

    def test_ge_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = class_under_test

        # Act
        actual: bool = class_under_test >= other

        # Assert
        self.assertTrue(actual)

    def test_ge_for_given_ids_returns_expected(self):
        param_list: list[tuple[int, int, bool]] = [
            # (self_)id, (other_)id, expected
            (0, 0, True),
            (1, 0, True),
            (0, 1, False),
        ]

        for self_id, other_id, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(self_id)
                other: Chapter = Chapter(other_id)

                # Act
                actual: bool = class_under_test >= other

                # Assert
                self.assertEqual(expected, actual)

    def test_gt_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = None

        # Act
        actual: bool = class_under_test > other

        # Assert
        self.assertTrue(actual)

    def test_gt_when_other_is_self_returns_false(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other: Chapter = class_under_test

        # Act
        actual: bool = class_under_test > other

        # Assert
        self.assertFalse(actual)

    def test_gt_for_given_ids_returns_expected(self):
        param_list: list[tuple[int, int, bool]] = [
            # (self_)id, (other_)id, expected
            (0, 0, False),
            (1, 0, True),
            (0, 1, False),
        ]

        for self_id, other_id, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(self_id)
                other: Chapter = Chapter(other_id)

                # Act
                actual: bool = class_under_test > other

                # Assert
                self.assertEqual(expected, actual)

    def test_le_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = None

        # Act
        actual: bool = class_under_test <= other

        # Assert
        self.assertTrue(actual)

    def test_le_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other: Chapter = class_under_test

        # Act
        actual: bool = class_under_test <= other

        # Assert
        self.assertTrue(actual)

    def test_le_for_given_ids_returns_expected(self):
        param_list: list[tuple[int, int, bool]] = [
            # (self_)id, (other_)id, expected
            (0, 0, True),
            (1, 0, False),
            (0, 1, True),
        ]

        for self_id, other_id, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(self_id)
                other: Chapter = Chapter(other_id)

                # Act
                actual: bool = class_under_test <= other

                # Assert
                self.assertEqual(expected, actual)

    def test_lt_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = None

        # Act
        actual: bool = class_under_test < other

        # Assert
        self.assertTrue(actual)

    def test_lt_when_other_is_self_returns_false(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other: Chapter = class_under_test

        # Act
        actual: bool = class_under_test < other

        # Assert
        self.assertFalse(actual)

    def test_lt_for_given_ids_returns_expected(self):
        param_list: list[tuple[int, int, bool]] = [
            # (self_)id, (other_)id, expected
            (0, 0, False),
            (1, 0, False),
            (0, 1, True),
        ]

        for self_id, other_id, expected in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(self_id)
                other: Chapter = Chapter(other_id)

                # Act
                actual: bool = class_under_test < other

                # Assert
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
