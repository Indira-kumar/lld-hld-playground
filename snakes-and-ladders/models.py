from dataclasses import dataclass


@dataclass
class Board:
    n: int
    special_chars: dict[int, int, SpecialChars]
    positions: list[list[list[Piece]]]

@dataclass
class Position:
    x: int
    y: int

@dataclass
class Piece:
    id: int
    player: Player
    color: str
    position: Position

@dataclass
class Player:
    name: str
    age: int
    gender: str
    color: str

@dataclass
class SpecialChars:
    start_pos: Position
    end_pos: Position
@dataclass
class Snake(SpecialChars):
    name: str = 'snake'
@dataclass
class Frog(SpecialChars):
    name: str = 'frog'
@dataclass
class Ladder(SpecialChars):
    name: str = 'ladder'

@dataclass
class Game:
    players: list[Player]
    pieces: dict[str, list[Piece]]
    board: Board
    snakes: list[Snake]
    frogs: list[Frog]
    ladders: list[Ladder]
    no_of_pieces: int