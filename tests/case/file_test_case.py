import os.path
import unittest
from io import TextIOWrapper
from typing import Any


class FileTestCase(unittest.TestCase):
    def assertFileEqual(self, expected: TextIOWrapper, actual: TextIOWrapper, msg: Any | None = None) -> None:
        expected_lines: list[str]
        actual_lines: list[str]

        try:
            expected_lines = expected.readlines()
            actual_lines = actual.readlines()
        finally:
            expected.close()
            actual.close()

        # Assert same number of lines
        expected_line_count: int = len(expected_lines)
        actual_line_count: int = len(actual_lines)

        if expected_line_count != actual_line_count:
            fail_msg: str = f'File does not have expected number of lines: expected {expected_line_count} was {actual_line_count}.'
            self.fail((msg + '\n' + fail_msg) if msg else fail_msg)

        # Assert same content length
        expected_content: str = ''.join(expected_lines)
        actual_content: str = ''.join(actual_lines)
        expected_length: int = len(expected_content)
        actual_length: int = len(actual_content)

        if expected_length != actual_length:
            fail_msg: str = f'File is not the same length as expected: expected {expected_length} was {actual_length}.'
            self.fail((msg + '\n' + fail_msg) if msg else fail_msg)

        # Assert same content
        if expected_content != actual_content:
            # Find first line with different content and report index of first difference
            idx: int = -1
            line_idx: int = 0

            while idx < 0 and line_idx < expected_line_count:
                expected_line: str = expected_lines[line_idx]
                actual_line: str = actual_lines[line_idx]
                line_idx += 1

                # Check indices for differences
                diff_indices: list[int] = [
                    i
                    for i in range(expected_line_count)
                    if expected_line[i] != actual_line[i]
                ]

                if len(diff_indices) < 1:
                    continue

                idx = diff_indices[0]

            fail_msg: str = f'File is different from expected on line {line_idx} at {idx}'
            self.fail((msg + '\n' + fail_msg) if msg else fail_msg)

    def assertFileExists(self, path: str, msg: Any | None = None) -> None:
        if not os.path.isfile(path):
            fail_msg: str = 'File does not exist.'
            self.fail((msg + '\n' + fail_msg) if msg else fail_msg)
