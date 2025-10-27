class Chapter:

    ### Constructors ###

    def __init__(self, init_id: int):
        self._id = init_id
        self._project_id = 0
        self._song_id = None
        self._speaker_id = 0
        self._subset = None

    ### Properties ###

    # Id
    @property
    def id(self) -> int:
        return self._id

    # ProjectId
    @property
    def project_id(self) -> int:
        return self._project_id

    @project_id.setter
    def project_id(self, value: int) -> None:
        self._project_id = value

    # SongId
    @property
    def song_id(self) -> str:
        return self._song_id

    @song_id.setter
    def song_id(self, value: str) -> None:
        self._song_id = value

    @song_id.deleter
    def song_id(self) -> None:
        del self._song_id

    # SpeakerId
    @property
    def speaker_id(self) -> int:
        return self._speaker_id

    @speaker_id.setter
    def speaker_id(self, value: int) -> None:
        self._speaker_id = value

    # Subset
    @property
    def subset(self) -> str:
        return self._subset

    @subset.setter
    def subset(self, value: str) -> None:
        self._subset = value

    ### Functions ###

    def __ge__(self, other):
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Chapter):
            return NotImplemented

        return self.id >= other.id

    def __gt__(self, other):
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Chapter):
            return NotImplemented

        return self.id > other.id

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if self is other:
            return True

        if not isinstance(other, Chapter):
            return False

        return (self.id == other.id
                and self.project_id == other.project_id
                and ((self.song_id is None and other.song_id is None)
                     or (self.song_id is not None and self.song_id == other.song_id))
                and self.speaker_id == other.speaker_id
                and ((self.subset is None and other.subset is None)
                     or (self.subset is not None and self.subset == other.subset)))

    def __hash__(self) -> int:
        return hash(self.id)

    def __le__(self, other):
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Chapter):
            return NotImplemented

        return self.id <= other.id

    def __lt__(self, other):
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Chapter):
            return NotImplemented

        return self.id < other.id

    def __str__(self) -> str:
        seperator = " | "
        str_list = [
            str(self.id), seperator,
            str(self.speaker_id), seperator,
            str(self.subset), seperator,
            str(self.project_id), seperator,
            str(self.song_id),
        ]

        return ''.join(str_list)
