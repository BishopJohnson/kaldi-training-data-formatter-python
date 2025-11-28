import os.path
from typing import Final

from kaldi_training_data_formatter import SpeakersReader, Speaker, SPEAKERS_FILENAME, CHAPTERS_FILENAME, ProjectUtil, \
    FilesUtil, Chapter, AUDIO_DIR_NAME


class ChaptersCompiler:
    # Information describing the chapters file and its layout
    __HEADER: Final[str] = (';\n' +
                            ';')

    def __init__(self, input_root: str, output_root: str):
        self.__input_root: str = input_root
        self.__output_root: str = output_root
        self.__chapters: list[Chapter] = []
        self.__song_id_length: int = 0  # The length of the longest song ID
        self.__subset_length: int = 0  # The length of the longest subset name

    @classmethod
    def from_root(cls, root: str):
        return cls(root, root)

    def compile_chapters(self) -> None:
        if not os.path.isdir(self.__input_root):
            raise Exception(f'Input root is not a directory: "{self.__input_root}"')

        # Get speakers from speakers file
        speakers_path: str = os.path.join(self.__input_root, SPEAKERS_FILENAME)

        if not os.path.isfile(speakers_path):
            raise Exception(f'Could not find speakers file in root input directory: "{self.__input_root}"')

        speakers: list[Speaker]

        with SpeakersReader(speakers_path) as reader:
            speakers = reader.read_all_speakers()

        # Visit each speaker's directory and get their associated chapters

        for speaker in speakers:
            # Validate speaker directory
            speaker_dir: str = os.path.join(self.__input_root, AUDIO_DIR_NAME, speaker.subset, str(speaker.speaker_id))
            print(speaker_dir)  # TODO

            if not os.path.isdir(speaker_dir):
                print(f'No such directory for speaker {speaker.speaker_id} at: "{speaker_dir}"')
                continue

            self.__subset_length = max(self.__subset_length, len(speaker.subset))

            # Get chapters for speaker
            transcript_paths: list[str] = FilesUtil.get_transcript_file_paths(speaker_dir)

            for path in transcript_paths:
                _, song_id = ProjectUtil.get_user_and_project_id(path)
                chapter: Chapter = Chapter(len(self.__chapters) + 1)
                chapter.speaker_id = speaker.speaker_id
                chapter.project_id = 1
                chapter.subset = speaker.subset
                chapter.song_id = song_id
                chapter.song_title = ProjectUtil.get_song_title(song_id)

                self.__chapters.append(chapter)
                self.__song_id_length = max(self.__song_id_length, len(song_id))

    def write_chapters(self) -> None:
        try:
            os.makedirs(self.__output_root, exist_ok=True)

            filepath: str = os.path.join(self.__output_root, CHAPTERS_FILENAME)

            with open(filepath, mode='w', encoding='utf-8') as file:  # Never write chapters with BOM
                file.write(ChaptersCompiler.__HEADER)
                file.write('\n')
                file.write(self.__create_column_headers())
                file.write('\n')

                for i in range(len(self.__chapters)):
                    file.write(self.__format_chapter(i + 1, self.__chapters[i]))
                    file.write('\n')
        except Exception as e:
            print('Error while writing chapters file: ' + str(e))

    def __create_column_headers(self) -> str:
        return (';ID    |SPEAKER|MINUTES| '
                + 'SUBSET'.ljust(self.__subset_length)
                + ' | PROJ | '
                + 'SONG ID'.ljust(self.__song_id_length)
                + ' | SONG TITLE')

    def __format_chapter(self, chapter_id: int, chapter: Chapter) -> str:
        return (str(chapter_id).ljust(6)  # Chapter ID
                + ' | '
                + str(chapter.speaker_id).ljust(5)  # Speaker ID
                + ' | 0.0   | '  # Minutes TODO: Use minutes property of Chapter.
                + chapter.subset.ljust(self.__subset_length)  # Subset
                + ' | 1    | '  # Project ID
                + chapter.song_id.ljust(self.__song_id_length)  # Song ID
                + ' | '
                + chapter.song_title)  # Song title
