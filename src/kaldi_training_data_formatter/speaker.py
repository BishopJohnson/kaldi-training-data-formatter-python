class Speaker:
    def __init__(self, init_id: int):
        self.__speaker_id: int = init_id
        self.__minutes: float = 0.0
        self.__name: str = ''
        self.__sex: str = ''
        self.__subset: str = ''

    @property
    def minutes(self) -> float:
        return self.__minutes

    @minutes.setter
    def minutes(self, value: float) -> None:
        self.__minutes = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def sex(self) -> str:
        return self.__sex

    @sex.setter
    def sex(self, value: str) -> None:
        self.__sex = value

    @property
    def speaker_id(self) -> int:
        return self.__speaker_id

    @speaker_id.setter
    def speaker_id(self, value: int) -> None:
        self.__speaker_id = value

    @property
    def subset(self) -> str:
        return self.__subset

    @subset.setter
    def subset(self, value: str) -> None:
        self.__subset = value

    @classmethod
    def from_line(cls, line: str):
        data: list[str] = [
            el.strip('\n\r\t ')
            for el in line.split('|')
        ]

        if len(data) < 5:
            raise Exception('Not enough elements on speakers line')

        speaker_id: int = int(data[0])
        speaker: Speaker = cls(speaker_id)
        speaker.sex = data[1]
        speaker.subset = data[2]
        speaker.minutes = float(data[3])
        speaker.name = data[4]

        return speaker

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if self is other:
            return True

        if not isinstance(other, Speaker):
            return False

        return (self.speaker_id == other.speaker_id
                and self.sex == other.sex
                and self.subset == other.subset
                and self.minutes == other.minutes
                and self.name == other.name)

    def __ge__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Speaker):
            raise NotImplemented

        return self.speaker_id >= other.speaker_id

    def __gt__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Speaker):
            raise NotImplemented

        return self.speaker_id > other.speaker_id

    def __hash__(self):
        return hash(self.speaker_id)

    def __le__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return True

        if not isinstance(other, Speaker):
            raise NotImplemented

        return self.speaker_id <= other.speaker_id

    def __lt__(self, other) -> bool:
        if other is None:
            return True

        if self is other:
            return False

        if not isinstance(other, Speaker):
            raise NotImplemented

        return self.speaker_id < other.speaker_id
