import os.path
from enum import Enum
from typing import Final

from kaldi_training_data_formatter import TranscriptLine, TranscriptReader, ProjectUtil
from kaldi_training_data_formatter.transcript_writer import TranscriptWriter


class FilesUtil:
    __EXTENSION: Final[str] = '.trans.txt'

    class __FormatType(Enum):
        Audio = 0
        Transcript = 1

    @staticmethod
    def format_audio_files(root: str, verbose: bool = False) -> None:
        FilesUtil.__format_files(root, FilesUtil.__FormatType.Audio, verbose=verbose)

    @staticmethod
    def format_transcript_files(root: str, verbose: bool = False) -> None:
        FilesUtil.__format_files(root, FilesUtil.__FormatType.Transcript, verbose=verbose)

    @staticmethod
    def __format_audio_files_for_transcript(transcript_path: str, verbose: bool = False) -> None:
        directory: str = os.path.dirname(transcript_path)

        if not directory:
            if verbose:
                print(f'Directory is not valid for transcript: "{transcript_path}"')
            return

        user_id, project_id = ProjectUtil.get_user_and_project_id(transcript_path)

        if not user_id or not project_id:
            if verbose:
                print(f'user_id or project_id are null or empty for transcript: "{transcript_path}"')
            return

        # Format audio files in directory
        flac_ext: str = '.flac'
        wav_ext: str = '.wav'
        files: set[str] = set()
        files.update([
            f.path
            for f in os.scandir(directory)
            if f.path.endswith(flac_ext) or f.path.endswith(wav_ext)
        ])
        unobserved_ids: set[str] = set()
        unobserved_ids.update(FilesUtil.__get_transcript_lines(transcript_path).keys())

        for file in files:
            filename, extension = os.path.splitext(os.path.basename(file))

            # Rename the file if the name is only a number (lacks user and project ID)
            line_id: int | None = int(filename) if filename.isdigit() else None

            if line_id is not None:
                filename = f'{user_id}-{project_id}-{str(line_id).zfill(4)}'  # Create the new filename
                os.rename(file, os.path.join(directory, filename + extension))

            # Try and mark the file as being observed
            if filename in unobserved_ids:
                unobserved_ids.remove(filename)

        # Check if the formatted file already exists
        unobserved_ids_list: list[str] = []
        unobserved_ids_list += unobserved_ids

        for el in unobserved_ids_list:
            flac_filename: str = os.path.join(directory, f'{el}{flac_ext}')
            wav_filename: str = os.path.join(directory, f'{el}{wav_ext}')

            if flac_filename in files or wav_filename in files:
                unobserved_ids.remove(el)

        if len(unobserved_ids) > 0 and verbose:
            print(f'Transcripts in {user_id}-{project_id} with unobserved files: [{", ".join(unobserved_ids)}]')

    @staticmethod
    def __format_files(root: str, format_type: __FormatType, verbose: bool = False) -> None:
        if not os.path.isdir(root):
            raise Exception(f'Given root is not a directory: "{root}"')

        directories_queue: list[str] = [root]

        while len(directories_queue) > 0:
            directory: str = directories_queue.pop()
            directories_queue += [f.path for f in os.scandir(directory) if f.is_dir()]
            has_transcript, transcript_path = FilesUtil.__has_transcript_file(directory)

            if not has_transcript:
                continue

            match format_type:
                case FilesUtil.__FormatType.Audio:
                    FilesUtil.__format_audio_files_for_transcript(transcript_path, verbose=verbose)
                case FilesUtil.__FormatType.Transcript:
                    FilesUtil.__format_transcript_files(transcript_path, verbose=verbose)
                case _:
                    raise Exception(f'Invalid format type {format_type}')

    @staticmethod
    def __format_transcript_files(transcript_path: str, verbose: bool = False) -> None:
        directory: str = os.path.dirname(transcript_path)

        if not directory:
            raise Exception(f'No valid directory for path: "{transcript_path}"')

        user_id, project_id = ProjectUtil.get_user_and_project_id(transcript_path)

        if not user_id or not project_id:
            raise Exception(f'Cannot determine user or project ID from path: "{transcript_path}"')

        filename: str = f'{user_id}-{project_id}{FilesUtil.__EXTENSION}'

        # Rename the transcript file if necessary
        if os.path.exists(transcript_path) and not transcript_path.endswith(filename):
            old_path: str = transcript_path
            transcript_path = os.path.join(directory, filename)
            os.rename(old_path, transcript_path)

            if verbose:
                print(f'Renamed transcript file at "{directory}" to "{filename}"')

        # Format the lines of the file
        old_lines: dict[str, TranscriptLine] = FilesUtil.__get_transcript_lines(transcript_path)
        new_lines: list[TranscriptLine] = []
        prefix: str = f'{user_id}-{project_id}-'
        prefix_length = len(prefix)
        do_formatting: bool = False

        for line_id, line in old_lines.items():
            if line_id.startswith(prefix) and (line_id[prefix_length:]).isdigit():
                new_lines.append(line)
                continue

            formatted_line_id: str = line_id.strip('[]')
            int_id: int | None = int(formatted_line_id) if formatted_line_id.isdigit() else None

            if int_id is None:
                raise Exception(f'Line with unknown format found in transcript file: "{transcript_path}"')

            new_lines.append(TranscriptLine(f'{prefix}{str(int_id).zfill(4)}', line.text))
            do_formatting = True

        if not do_formatting:
            return

        writer: TranscriptWriter = TranscriptWriter(directory)
        writer.write_transcript(filename, new_lines)

        if verbose:
            print(f'Reformatted transcript file "{transcript_path}"')

    @staticmethod
    def __get_transcript_lines(transcript_path: str) -> dict[str, TranscriptLine]:
        lines: dict[str, TranscriptLine] = {}

        with TranscriptReader(transcript_path) as reader:
            line: TranscriptLine

            while line := reader.read_transcript_line():
                if line.id in lines.keys():
                    pass  # TODO: Handle duplicate IDs.
                else:
                    lines[line.id] = line

        return lines

    @staticmethod
    def __has_transcript_file(directory: str) -> tuple[bool, str | None]:
        files: list[str] = [
            f.path
            for f in os.scandir(directory)
            if f.is_file() and f.path.endswith(FilesUtil.__EXTENSION)
        ]

        if len(files) > 0:
            return True, files[0]
        else:
            return False, None
