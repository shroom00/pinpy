from dataclasses import dataclass, field


@dataclass
class Pin:
    """Class representing a Pinterest pin."""
    title: str
    description: str
    images: list[dict] = field(repr=False)
    url: str
    content_url: str = field(repr=False)
    pin_id: int
    created_at: str = field(repr=False)
    colour: str = field(repr=False)
    pinner_name: str
    pinner_id: int = field(repr=False)
    board_name: str = field(repr=False)
    board_id: int = field(repr=False)
    board_url: str

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