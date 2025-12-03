import argparse
import os.path
import shutil
import traceback

from kaldi_training_data_formatter import \
    VocabCompiler, \
    FilesUtil, \
    LexiconCompiler, \
    SubsetSorter, \
    ChaptersCompiler, \
    AUDIO_DIR_NAME, \
    SpeakersReader, \
    Speaker


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
        parser.add_argument('-v',
                            '--validate',
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
        parser.add_argument('--test-speakers',
                            type=float,
                            help=('The number or ratio of speakers to be used in the test subset.'
                                  + ' Integers greater than or equal to 1 will specify the number of speakers. '
                                  + ' Values between [0.0, 1.0) will specify the ratio of speakers.'))
        self.__args = parser.parse_args()
        self.__root: str = self.__args.root if self.__args.root else os.getcwd()
        self.__audio_root: str = os.path.join(self.__root, AUDIO_DIR_NAME)
        self.__verbose: bool = self.__args.verbose

    def run(self) -> int:
        try:
            compile_flag: bool | None = self.__args.compile
            format_flag: bool | None = self.__args.format
            sort_flag: bool | None = self.__args.sort
            validate_flag: bool | None = self.__args.validate

            if format_flag:
                self.__format_transcript_files()

            if compile_flag:
                self.__compile_lexicon_and_vocab()

            if format_flag:
                self.__format_audio_files()

            if sort_flag:
                self.__sort_subsets()

            if validate_flag:
                self.__validate_speaker_chapters()

            if compile_flag:
                self.__compile_chapters()

            return 0
        except Exception:
            print(traceback.format_exc())
            return -1

    def __compile_chapters(self) -> None:
        print('Compiling chapter file')
        chapters_compiler: ChaptersCompiler = ChaptersCompiler.from_root(self.__root)
        chapters_compiler.compile_chapters()
        chapters_compiler.write_chapters()

    def __compile_lexicon_and_vocab(self) -> None:
        print('Compiling vocabulary and lexicon files')
        vocab_compiler: VocabCompiler = VocabCompiler.from_root(self.__root)
        vocab_compiler.verbose = self.__verbose
        vocab_compiler.read_vocabulary()
        vocab_compiler.save_vocabulary()

        lexicon_compiler: LexiconCompiler = LexiconCompiler.from_root(self.__root)
        lexicon_compiler.verbose = self.__verbose
        lexicon_compiler.set_import_lexicons(self.__args.import_lexicons)
        lexicon_compiler.compile_lexicon(vocab_compiler.vocabulary, use_existing=True)
        lexicon_compiler.save_lexicon()

    def __format_audio_files(self) -> None:
        print('Formatting audio files')
        FilesUtil.format_audio_files(self.__audio_root, verbose=self.__verbose)

    def __format_transcript_files(self) -> None:
        print('Formatting transcript files')
        FilesUtil.format_transcript_files(self.__audio_root, verbose=self.__verbose)

    def __sort_subsets(self) -> None:
        print('Sorting data into subsets')
        test_speakers: float | None = self.__args.test_speakers
        sorter: SubsetSorter = (SubsetSorter.builder()
                                .set_input_root(self.__root)
                                .set_output_root(self.__root)
                                .build())
        sorter.gather_sources()

        if test_speakers:
            sorter.sort_sources(test_speakers=self.__args.test_speakers)
        else:
            sorter.sort_sources()

    def __validate_speaker_chapters(self) -> None:
        print('Validating speaker chapters')
        speakers: list[Speaker]

        with SpeakersReader(self.__root) as reader:
            speakers = reader.read_all_speakers()

        for speaker_idx in range(len(speakers)):
            speaker: Speaker = speakers[speaker_idx]
            speaker_path: str = os.path.join(self.__audio_root, speaker.subset, str(speaker.speaker_id))
            speaker_transcripts: list[str] = FilesUtil.get_transcript_file_paths(speaker_path)

            for transcript_idx in range(len(speaker_transcripts)):
                transcript_path: str = speaker_transcripts[transcript_idx]

                # Remove chapter directory if not all audio files are present
                if FilesUtil.has_all_audio_files_for_transcript(transcript_path):
                    continue

                directory: str = os.path.join(speaker_path, os.path.dirname(transcript_path))
                shutil.rmtree(directory)

                del speaker_transcripts[transcript_idx]
                transcript_idx -= 1

                if self.__verbose:
                    print(f'Removed empty chapters directory: {directory}')


def cli() -> int:
    return App().run()
