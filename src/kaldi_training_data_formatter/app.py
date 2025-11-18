import argparse
import os.path
import traceback

from kaldi_training_data_formatter import VocabCompiler, FilesUtil, LexiconCompiler


class App:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c',
                            '--compile',
                            action='store_true')
        parser.add_argument('-f',
                            '--format',
                            action='store_true')
        parser.add_argument('-s',
                            '--sort',
                            action='store_true')
        parser.add_argument('--import-lexicons',
                            type=str,
                            nargs='+',
                            help='The filename(s) of the lexicon(s) to import phones from.')
        parser.add_argument('--verbose',
                            action='store_true')
        parser.add_argument('--root',
                            type=str,
                            help='The root directory to run the app in.')
        self.__args = parser.parse_args()

    def run(self) -> int:
        try:
            root: str = self.__args.root if self.__args.root else os.getcwd()
            audio_root: str = os.path.join(root, 'audio')
            verbose: bool = self.__args.verbose

            if self.__args.compile:  # Compile vocabulary and lexicon
                if self.__args.format:
                    print('Formatting transcript files')
                    FilesUtil.format_transcript_files(audio_root, verbose=verbose)

                print('Compiling vocabulary and lexicon files')
                vocab_compiler: VocabCompiler = VocabCompiler.from_root(root)
                vocab_compiler.verbose = verbose
                vocab_compiler.read_vocabulary()
                vocab_compiler.save_vocabulary()

                lexicon_compiler: LexiconCompiler = LexiconCompiler.from_root(root)
                lexicon_compiler.verbose = verbose
                lexicon_compiler.set_import_lexicons(self.__args.import_lexicons)
                lexicon_compiler.compile_lexicon(vocab_compiler.vocabulary, use_existing=True)
                lexicon_compiler.save_lexicon()

            FilesUtil.format_audio_files(audio_root, verbose=self.__verbose)
            if self.__args.format:
                print('Formatting audio files')
                FilesUtil.format_audio_files(audio_root, verbose=verbose)

            if self.__args.sort:
                print('Sorting data into subsets')

            return 0
        except Exception:
            print(traceback.format_exc())
            return -1


def cli() -> int:
    return App().run()
