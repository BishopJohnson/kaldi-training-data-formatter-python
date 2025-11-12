import argparse
import os.path

from kaldi_training_data_formatter import VocabCompiler, FilesUtil, LexiconCompiler


class App:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--import-lexicon',
                            type=str,
                            help='The filename of the lexicon to import phones from.')
        parser.add_argument('-v',
                            '--verbose',
                            action='store_true')
        parser.add_argument('-r',
                            '--root',
                            type=str,
                            help='The root directory to run the app in.')
        args = parser.parse_args()

        self.__root: str = args.root if args.root else os.getcwd()
        self.__lexicon_compiler: LexiconCompiler = LexiconCompiler.from_root(self.__root,
                                                                             True,
                                                                             import_name=args.import_lexicon)
        self.__vocab_compiler: VocabCompiler = VocabCompiler.from_root(self.__root)

    def run(self) -> int:
        audio_root: str = os.path.join(self.__root, 'audio')

        self.__vocab_compiler.read_vocabulary()
        self.__vocab_compiler.save_vocabulary()
        self.__lexicon_compiler.compile_lexicon(self.__vocab_compiler.vocabulary)
        self.__lexicon_compiler.save_lexicon()

        FilesUtil.format_audio_files(audio_root)

        return 0


def cli() -> int:
    return App().run()
