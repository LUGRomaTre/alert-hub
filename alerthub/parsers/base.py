from abc import ABC, abstractmethod
from datetime import datetime
from typing import NamedTuple


class Article(NamedTuple):
    text: str
    id: int = 0
    title: str = None
    datetime: datetime = None


class Parser(ABC):
    @abstractmethod
    def run(self):
        pass

    @property
    @abstractmethod
    def channel_name(self):
        pass
