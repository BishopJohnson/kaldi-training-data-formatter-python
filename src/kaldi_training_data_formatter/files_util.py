import os.path
import shutil
from enum import Enum

from kaldi_training_data_formatter import TranscriptLine, \
    TranscriptReader, \
    ProjectUtil, \
    TRANSCRIPT_EXT, \
    FLAC_EXT, \
    WAV_EXT
from kaldi_training_data_formatter.transcript_writer import TranscriptWriter


class FilesUtil:
    class __FormatType(Enum):
        Audio = 0
        Transcript = 1

    @staticmethod
    def format_audio_files(root: str, verbose: bool = False) -> None:
        FilesUtil.__format_files(root, FilesUtil.__FormatType.Audio, verbose=verbose)

    @staticmethod
    def format_paths(root: str, verbose: bool = False) -> None:
        if not os.path.isdir(root):
            raise Exception(f'Given root is not a directory: "{root}"')

        directories_queue: list[str] = [root]

        while len(directories_queue) > 0:
            directory: str = directories_queue.pop()

            # Format directory name
            parent, basename = os.path.split(directory)
            old: str = directory
            directory = os.path.join(parent, basename.lower())
            shutil.move(old, directory)

            # Queue subdirectories and rename files
            for path in os.scandir(directory):
                if path.is_dir():
                    directories_queue.append(path.path)
                elif path.is_file():
                    filepath: str = path.path
                    _, filename_and_ext = os.path.split(filepath)
                    filename: str
                    ext: str

                    if filename_and_ext.endswith(TRANSCRIPT_EXT):
                        ext = TRANSCRIPT_EXT
                        filename = filename_and_ext[0:len(ext)]
                    else:
                        filename, ext = os.path.splitext(filename_and_ext)

                    new_filepath: str = os.path.join(directory, filename.lower() + ext)
                    shutil.move(filepath, new_filepath)

    @staticmethod
    def format_transcript_files(root: str, verbose: bool = False) -> None:
        FilesUtil.__format_files(root, FilesUtil.__FormatType.Transcript, verbose=verbose)

    @staticmethod
    def get_transcript_file_paths(root: str) -> list[str]:
        paths: list[str] = []
        directories: list[str] = [root]

        while len(directories) > 0:
            directory: str = directories.pop()

            if not os.path.isdir(directory):
                continue

            for f in os.scandir(directory):
                if f.is_dir():
                    directories.append(f.path)
                elif f.is_file() and f.path.endswith(TRANSCRIPT_EXT):
                    paths.append(f.path)

        return paths

    @staticmethod
    def has_all_audio_files_for_transcript(transcript_path: str, verbose: bool = False) -> bool:
        directory, _ = os.path.split(transcript_path)

        if not directory:
            if verbose:
                print(f'Directory is not valid for transcript: "{transcript_path}"')

            return False

        lines: dict[str, TranscriptLine] = FilesUtil.__get_transcript_lines(transcript_path)

        for line in lines:
            line_path: str = os.path.join(directory, line)
            line_flac_path: str = line_path + FLAC_EXT
            line_wav_path: str = line_path + WAV_EXT

            if not os.path.isfile(line_flac_path) and not os.path.isfile(line_wav_path):
                if verbose:
                    print(f'No audio file for transcript line at: {line_path}.*')

                return False

        return True

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
        files: set[str] = set()
        files.update([
            f.path
            for f in os.scandir(directory)
            if f.path.endswith(FLAC_EXT) or f.path.endswith(WAV_EXT)
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
            flac_filename: str = os.path.join(directory, el + FLAC_EXT)
            wav_filename: str = os.path.join(directory, el + WAV_EXT)

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
            directories_queue.extend([f.path for f in os.scandir(directory) if f.is_dir()])
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

        filename: str = f'{user_id}-{project_id}{TRANSCRIPT_EXT}'

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
            if f.is_file() and f.path.endswith(TRANSCRIPT_EXT)
        ]

        if len(files) > 0:
            return True, files[0]
        else:
            return False, None
