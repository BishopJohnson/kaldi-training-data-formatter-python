import os.path
from typing import Final, Collection

from kaldi_training_data_formatter import SPEAKERS_FILENAME, Speaker


class SpeakersWriter:
    __HEADER: Final[str] = ('; id: The ID of the person in the audio\n' +
                            '; sex: \'F\' for female, \'M\' for male\n' +
                            '; - Add \'X\' for "prefer not to say" if Vosk is updated to support it)\n' +
                            '; subset:\n' +
                            '; name: The provided name of the person\n' +
                            ';')

    def __init__(self):
        self.__subset_length: int = 0

    def write_speakers(self, root: str, speakers: Collection[Speaker]) -> bool:
        if not os.path.isdir(root):
            raise Exception(f'Given root is not a directory: {root}')

        filepath: str = os.path.join(root, SPEAKERS_FILENAME)
        self.__subset_length = max(0, max([
            len(s.subset)
            for s in speakers
        ]))

        try:
            with open(filepath, mode='w', encoding='utf-8') as f:
                f.write(SpeakersWriter.__HEADER)
                f.write('\n')
                f.write(self.__create_column_headers())
                f.write('\n')

                for speaker in speakers:
                    f.write(self.__format_speaker(speaker))
                    f.write('\n')
        except Exception as e:
            print('Error while writing speaker file: ' + str(e))
            return False

        return True

    def __create_column_headers(self) -> str:
        return (';ID  |SEX| '
                + 'SUBSET'.ljust(self.__subset_length)
                + ' |MINUTES| NAME')

    def __format_speaker(self, speaker: Speaker) -> str:
        return (str(speaker.speaker_id).ljust(4)
                + ' | '
                + speaker.sex
                + ' | '
                + speaker.subset.ljust(self.__subset_length)
                + ' | '
                + '{:.1f}'.format(speaker.minutes).ljust(5)
                + ' | '
                + speaker.name)
