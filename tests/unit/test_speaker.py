import unittest

from kaldi_training_data_formatter import Speaker


class TestSpeaker(unittest.TestCase):
    def test_eq_when_other_is_none_returns_false(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = None

        # Act
        actual: bool = class_under_test == other

        # Assert
        self.assertFalse(actual)

    def test_eq_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
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
                class_under_test: Speaker = Speaker(ids)
                other: Speaker = Speaker(ids)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertTrue(actual)

    def test_eq_when_other_has_different_id_returns_false(self):
        param_list: list[tuple[int, int]] = [
            # (self_)id, (other_)id
            (0, 1),
            (1, 0),
        ]

        for self_id, other_id in param_list:
            with self.subTest():
                # Arrange
                class_under_test: Speaker = Speaker(self_id)
                other: Speaker = Speaker(other_id)

                # Act
                actual: bool = class_under_test == other

                # Assert
                self.assertFalse(actual)

    def test_ge_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = None

        # Act
        actual: bool = class_under_test >= other

        # Assert
        self.assertTrue(actual)

    def test_ge_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
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
                class_under_test: Speaker = Speaker(self_id)
                other: Speaker = Speaker(other_id)

                # Act
                actual: bool = class_under_test >= other

                # Assert
                self.assertEqual(expected, actual)

    def test_gt_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = None

        # Act
        actual: bool = class_under_test > other

        # Assert
        self.assertTrue(actual)

    def test_gt_when_other_is_self_returns_false(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = class_under_test

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
                class_under_test: Speaker = Speaker(self_id)
                other: Speaker = Speaker(other_id)

                # Act
                actual: bool = class_under_test > other

                # Assert
                self.assertEqual(expected, actual)

    def test_le_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = None

        # Act
        actual: bool = class_under_test <= other

        # Assert
        self.assertTrue(actual)

    def test_le_when_other_is_self_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = class_under_test

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
                class_under_test: Speaker = Speaker(self_id)
                other: Speaker = Speaker(other_id)

                # Act
                actual: bool = class_under_test <= other

                # Assert
                self.assertEqual(expected, actual)

    def test_lt_when_other_is_none_returns_true(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = None

        # Act
        actual: bool = class_under_test < other

        # Assert
        self.assertTrue(actual)

    def test_lt_when_other_is_self_returns_false(self):
        # Arrange
        class_under_test: Speaker = Speaker(0)
        other = class_under_test

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
                class_under_test: Speaker = Speaker(self_id)
                other: Speaker = Speaker(other_id)

                # Act
                actual: bool = class_under_test < other

                # Assert
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
