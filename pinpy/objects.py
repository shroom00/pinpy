from dataclasses import dataclass, field
from typing import List, Optional
from . import utils


@dataclass
class Pin:
    """Class representing a Pinterest pin."""

    _session: object = field(repr=False)
    title: str
    description: str
    images: list[dict] | str = field(repr=False)
    video_url: str = field(repr=False)
    url: str
    pin_id: int = field(repr=False)
    created_at: str = field(repr=False)
    colour: str = field(repr=False)
    pinner_name: str
    pinner_id: int = field(repr=False)
    board_name: str = field(repr=False)
    board_id: int = field(repr=False)
    board_url: str
    media_type: str

    def download(self, filepath: str = "") -> str:
        return utils.download_pin(self, filepath)

    def __hash__(self) -> int:
        return self.pin_id


@dataclass
class User:
    """Class representing a Pinterest user."""

    pass


@dataclass
class Board:
    """Class representing a Pinterest board."""

    pass


@dataclass
class Results:
    """Class representing a page of pins e.g. homefeed, search"""

    _client: object
    query: str
    scope: str
    pins: List[Pin]
    bookmark: str
    next_bookmark: str

    def next_page(self) -> Optional["Results"]:
        if self.next_bookmark == "-end-":
            return None
        return self._client.search(self.query, self.scope, self.next_bookmark)

    def __getitem__(self, index: int) -> Pin:
        return self.pins[index]

    def __len__(self):
        return len(self.pins)
