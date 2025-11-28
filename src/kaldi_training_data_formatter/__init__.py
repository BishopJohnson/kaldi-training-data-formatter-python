from typing import Final

AUDIO_DIR_NAME: Final[str] = 'audio'
CHAPTERS_FILENAME: Final[str] = 'CHAPTERS.TXT'
LEXICON_FILENAME: Final[str] = 'lexicon.txt'
NO_PHONES_VALUE: Final[str] = '<<<<<!!! NO PHONES !!!>>>>>'
SPEAKERS_FILENAME: Final[str] = 'SPEAKERS.TXT'
TRANSCRIPT_EXT: Final[str] = '.trans.txt'
VOCAB_FILENAME: Final[str] = 'vocab.txt'

# No dependencies
from .transcript_line import TranscriptLine
from .project_util import ProjectUtil

# Models
from .speaker import Speaker
from .chapter import Chapter  # Depends on speaker

# Depends on the above
from .abstract_file_reader import AbstractFileReader
from .transcript_reader import TranscriptReader

# Depends on the above
from .files_util import FilesUtil

# Depends on the above
from .chapters_compiler import ChaptersCompiler
from .lexicon_compiler import LexiconCompiler
from .vocab_compiler import VocabCompiler

# Import app last
from .app import App
