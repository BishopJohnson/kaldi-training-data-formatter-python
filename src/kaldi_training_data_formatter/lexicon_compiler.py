import os.path
from typing import Final, Collection


class LexiconCompiler:
    LEXICON_FILENAME: Final[str] = 'lexicon.txt'

    def __init__(self, input_root: str, output_root: str, use_existing: bool = False, import_name: str | None = None):
        self.__input_root: Final[str] = input_root
        self.__output_root: Final[str] = output_root
        self.__use_existing: Final[bool] = use_existing
        self.__import_name: Final[str | None] = import_name
        self.__lexicon: Final[dict[str, set[str]]] = {}

    @classmethod
    def from_root(cls, root: str, use_existing: bool = False, import_name: str | None = None):
        return cls(root, root, use_existing, import_name)

    @property
    def import_lexicon_name(self) -> str | None:
        return self.__import_name

    @property
    def lexicon(self) -> dict[str, set[str]]:
        return self.__lexicon

    def compile_lexicon(self, vocabulary: Collection[str]) -> None:
        temp_lexicon: dict[str, set[str]] = {}
        self.__lexicon.clear()

        # Read from imported lexicon
        if self.import_lexicon_name:
            path: str = os.path.join(self.__input_root, self.import_lexicon_name)
            LexiconCompiler.__read_lexicon(path, temp_lexicon)

        # Read from existing lexicon
        if self.__use_existing:
            path: str = os.path.join(self.__input_root, LexiconCompiler.LEXICON_FILENAME)
            LexiconCompiler.__read_lexicon(path, temp_lexicon)

        # Read vocabulary
        for vocab in vocabulary:
            # Only keep entries that appear in vocabulary
            self.__lexicon[vocab] = temp_lexicon[vocab] if vocab in temp_lexicon else set()

    def save_lexicon(self) -> None:
        words: list[str] = []
        words += self.__lexicon.keys()
        words.sort()

        filepath: str = os.path.join(self.__output_root, LexiconCompiler.LEXICON_FILENAME)

        try:
            os.makedirs(self.__output_root, exist_ok=True)

            with open(filepath, mode='w', encoding='utf-8') as f:  # Never write lexicon with BOM
                for word in words:
                    phones: list[str] = []
                    phones += self.__lexicon[word]
                    phones.sort()

                    if len(phones) > 0:
                        for phone in phones:
                            f.write(word)
                            f.write(' ')
                            f.write(phone)
                            f.write('\n')
                    else:
                        f.write(word)
                        f.write(' ')
                        f.write('<<<<<!!! NO PHONES !!!>>>>>')
                        f.write('\n')
        except Exception as e:
            print('Error while saving lexicon file: ' + str(e))

    @staticmethod
    def __read_lexicon(path: str, write_lexicon: dict[str, set[str]]) -> None:
        if not os.path.isfile(path):
            return

        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                line_num: int = 0

                while line := f.readline():
                    elements: list[str] = [
                        el
                        for el in [token.strip('\n\r ') for token in line.replace('\t', ' ').split(' ')]
                        if len(el) > 0
                    ]
                    line_num += 1

                    if len(elements) < 2:
                        print(f'Too few elements on line {line_num} in lexicon: "{path}"')
                        continue

                    word: str = elements[0].lower()
                    phones: str = ' '.join(elements[1:]).upper()
                    existing_phones: set[str]

                    if word in write_lexicon:
                        existing_phones = write_lexicon[word]
                    else:
                        existing_phones = set()
                        write_lexicon[word] = existing_phones

                    existing_phones.add(phones)
        except Exception as e:
            print('Error while reading lexicon file: ' + str(e))
