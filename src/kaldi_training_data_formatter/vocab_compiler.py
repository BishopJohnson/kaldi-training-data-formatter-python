import os.path
from typing import Final

from kaldi_training_data_formatter import ProjectUtil


class VocabCompiler:
    VOCAB_FILENAME: Final[str] = 'vocab.txt'

    def __init__(self, input_root: str, output_root: str):
        self.__input_root: Final[str] = input_root
        self.__output_root: Final[str] = output_root
        self.__vocabulary: Final[set[str]] = set()

    @classmethod
    def from_root(cls, root: str):
        return cls(root, root)

    @property
    def vocabulary(self) -> set[str]:
        return self.__vocabulary

    def read_vocabulary(self) -> None:
        self.vocabulary.clear()

        if not os.path.isdir(self.__input_root):
            raise Exception(f'Directory does not exist: "{self.__input_root}"')

        visited_projects: set[str] = set()
        directory_queue: list[str] = [self.__input_root]

        while len(directory_queue) > 0:
            directory: str = directory_queue.pop()

            if not os.path.isdir(directory):
                print(f'Could not find directory: "{directory}"')
                continue

            entries: list[str] = [os.path.join(directory, f) for f in os.listdir(directory)]
            files: list[str] = [f for f in entries if os.path.isfile(f) and f.endswith('.trans.txt')]
            file: str | None = files[0] if len(files) > 0 else None

            # If no transcript file was found then try adding subdirectories and skip this directory
            if not file:
                directory_queue += [d for d in entries if os.path.isdir(d)]
                continue

            # Add project name to set of visited projects
            _, project_id = ProjectUtil.get_user_and_project_id(directory)

            if project_id in visited_projects:
                continue  # Skip if already visited

            visited_projects.add(project_id)

            # Read vocabulary from transcript file
            with open(file, mode='r', encoding='utf-8-sig') as f:
                line: str

                while line := f.readline():
                    self.vocabulary.update(line.strip('\n\r ').lower().split(' ')[1:])

    def save_vocabulary(self) -> None:
        filepath: str = os.path.join(self.__output_root, VocabCompiler.VOCAB_FILENAME)
        sorted_vocab: list[str] = []
        sorted_vocab += self.vocabulary
        sorted_vocab.sort()

        try:
            os.makedirs(self.__output_root, exist_ok=True)

            with open(filepath, mode='w', encoding='utf-8') as f:  # Never write vocabulary with BOM
                for vocab in sorted_vocab:
                    f.write(vocab)
                    f.write('\n')
        except Exception as e:
            print(f'Error while saving vocabulary file: ' + str(e))
