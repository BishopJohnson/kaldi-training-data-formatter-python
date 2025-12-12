import unittest

from kaldi_training_data_formatter import ProjectUtil


class TestProjectUtil(unittest.TestCase):
    def test_get_song_title_given_song_id_returns_expected(self):
        param_list: list[tuple[str, str]] = [
            # song_id, expected
            ('', ''),
            ('ABOVE-BELOW_CVRD-438', 'ABOVE BELOW'),
            ('ABOVE-BELOW_CVRD-438_Player-1', 'ABOVE BELOW'),
        ]

        for song_id, expected in param_list:
            with self.subTest():
                # Act
                actual: str = ProjectUtil.get_song_title(song_id)

                # Assert
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
