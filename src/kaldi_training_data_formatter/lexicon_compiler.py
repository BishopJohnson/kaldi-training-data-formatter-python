import os.path
from typing import Final, Collection


class LexiconCompiler:
    LEXICON_FILENAME: Final[str] = 'lexicon.txt'

    def __init__(self, input_root: str, output_root: str):
        self.__input_root: Final[str] = input_root
        self.__output_root: Final[str] = output_root
        self.__import_lexicons: Final[list[str]] = []
        self.__lexicon: Final[dict[str, set[str]]] = {}
        self.__verbose: bool = False

    @classmethod
    def from_root(cls, root: str):
        return cls(root, root)

    @property
    def lexicon(self) -> dict[str, set[str]]:
        return self.__lexicon

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self.__verbose = value

    def compile_lexicon(self, vocabulary: Collection[str], use_existing: bool = False) -> None:
        temp_lexicon: dict[str, set[str]] = {}
        self.__lexicon.clear()

        # Read from imported lexicon
        for lexicon in self.__import_lexicons:
            path: str = os.path.join(self.__input_root, lexicon)
            LexiconCompiler.__read_lexicon(path, temp_lexicon)

        # Read from existing lexicon
        if use_existing:
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
                line_count: int = 1

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

                            line_count += 1
                    else:
                        f.write(word)
                        f.write(' ')
                        f.write('<<<<<!!! NO PHONES !!!>>>>>')
                        f.write('\n')
                        print(f'Wrote word "{word}" with no phones on line {line_count} to lexicon')

                        line_count += 1
        except Exception as e:
            print('Error while saving lexicon file: ' + str(e))

    def set_import_lexicons(self, lexicons: Collection[str] | str | None) -> None:
        self.__import_lexicons.clear()

        if type(lexicons) is str:
            self.__import_lexicons.append(lexicons)
        elif type(lexicons) is Collection[str]:
            self.__import_lexicons.extend(lexicons)

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
