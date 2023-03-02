from dataclasses import dataclass, field
from typing import List


@dataclass
class Pin:
    """Class representing a Pinterest pin."""

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

    def __hash__(self) -> int:
        return self.pin_id


@dataclass
class User:
    """Class representing a Pinterest user."""

    pass


@dataclass
class Board:
    """Class representing a Pinterest board."""

    name: str
    description: str
    url: str
    pin_count: int
    board_id: int
    owner: str  # username?
    followed: bool
    collaborative: bool
    privacy: str

    def __len__(self) -> int:
        return self.pin_count


@dataclass
class Results:
    """Class representing a page of results e.g. homefeed, search"""

    _query: str
    _scope: str
    results: List[Pin | Board]
    warnings: dict
    _bookmark: str = field(repr=False)
    _next_bookmark: str = field(repr=False)

    def __getitem__(self, index: int) -> Pin:
        return self.results[index]

    def __len__(self):
        return len(self.results)
