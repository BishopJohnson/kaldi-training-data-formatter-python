import unittest

from kaldi_training_data_formatter import Chapter


class TestChapter(unittest.TestCase):
    def test_eq_when_other_is_none_returns_false(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = None

        # Act
        actual: bool = class_under_test == other

        # Assert
        self.assertFalse(actual)

    def test_eq_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Chapter = Chapter(0)
        other = class_under_test

        # Act
        actual: bool = class_under_test == other

        # Assert
        self.assertTrue(actual)

    def test_eq_when_other_has_same_id_returns_true(self):
        param_list: list[int] = [0, 1]

        for ids in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(ids)
                other: Chapter = Chapter(ids)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertTrue(actual, f'Assert that "{ids} == {ids}" is True')

    def test_eq_when_other_has_different_id_returns_false(self):
        param_list: list[tuple[int, int]] = [
            # (self_)id, (other_)id
            (0, 1),
            (1, 0),
        ]

        for self_id, other_id in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Chapter = Chapter(self_id)
                other: Chapter = Chapter(other_id)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertFalse(actual, f'Assert that "{self_id} == {other_id}" is False')

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
                self.assertEqual(expected, actual, f'Assert that "{self_id} >= {other_id}" is {str(expected)}')

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
                self.assertEqual(expected, actual, f'Assert that "{self_id} > {other_id}" is {str(expected)}')

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
                self.assertEqual(expected, actual, f'Assert that "{self_id} <= {other_id}" is {str(expected)}')

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
                self.assertEqual(expected, actual, f'Assert that "{self_id} < {other_id}" is {str(expected)}')


if __name__ == '__main__':
    unittest.main()
