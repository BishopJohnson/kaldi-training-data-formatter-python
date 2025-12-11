class Chapter:
    def __init__(self, init_id: int):
        self.__id: int = init_id
        self.__minutes: float = 0.0
        self.__project_id: int = 0
        self.__song_id: str | None = None
        self.__song_title: str | None = None
        self.__speaker_id: int = 0
        self.__subset: str | None = None

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def minutes(self) -> float:
        return self.__minutes

    @minutes.setter
    def minutes(self, value: float) -> None:
        self.__minutes = value

    @property
    def project_id(self) -> int:
        return self.__project_id

    @project_id.setter
    def project_id(self, value: int) -> None:
        self.__project_id = value

    @property
    def song_id(self) -> str | None:
        return self.__song_id

    @song_id.setter
    def song_id(self, value: str) -> None:
        self.__song_id = value

    @song_id.deleter
    def song_id(self) -> None:
        del self.__song_id

    @property
    def song_title(self) -> str | None:
        return self.__song_title

    @song_title.setter
    def song_title(self, value: str) -> None:
        self.__song_title = value

    @property
    def speaker_id(self) -> int:
        return self.__speaker_id

    @speaker_id.setter
    def speaker_id(self, value: int) -> None:
        self.__speaker_id = value

    @property
    def subset(self) -> str | None:
        return self.__subset

    @subset.setter
    def subset(self, value: str) -> None:
        self.__subset = value

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

    def __ge__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Chapter):
            raise NotImplemented

        # ID
        if self.id < other.id:
            return False

        if self.id > other.id:
            return True

        # Speaker ID
        if self.speaker_id < other.speaker_id:
            return False

        if self.speaker_id > other.speaker_id:
            return True

        # Song title
        if self.song_title is None:
            return other.song_title is None

        if other.song_title is None:
            return True

        return self.song_title >= other.song_title

    def __gt__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Chapter):
            raise NotImplemented

        # ID
        if self.id < other.id:
            return False

        if self.id > other.id:
            return True

        # Speaker ID
        if self.speaker_id < other.speaker_id:
            return False

        if self.speaker_id > other.speaker_id:
            return True

        # Song title
        if self.song_title is None:
            return False

        if other.song_title is None:
            return True

        return self.song_title > other.song_title

    def __le__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Chapter):
            raise NotImplemented

        # ID
        if self.id < other.id:
            return True

        if self.id > other.id:
            return False

        # Speaker ID
        if self.speaker_id < other.speaker_id:
            return True

        if self.speaker_id > other.speaker_id:
            return False

        # Song title
        if self.song_title is None:
            return other.song_title is None

        if other.song_title is None:
            return False

        return self.song_title <= other.song_title

    def __lt__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Chapter):
            raise NotImplemented

        # ID
        if self.id < other.id:
            return True

        if self.id > other.id:
            return False

        # Speaker ID
        if self.speaker_id < other.speaker_id:
            return True

        if self.speaker_id > other.speaker_id:
            return False

        # Song title
        if self.song_title is None:
            return not other.song_title is None

        if other.song_title is None:
            return False

        return self.song_title < other.song_title
