from dataclasses import dataclass


@dataclass
class Board:
    n: int

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
class Snake:
    start_pos: Position
    end_pos: Position

@dataclass
class Frog:
    start_pos: Position
    end_pos: Position

@dataclass
class Ladder:
    start_pos: Position
    end_pos: Position

@dataclass
class Game:
    players: list[Player]
    pieces: list[Piece]
    board: Board
    snakes: list[Snake]
    frogs: list[Frog]
    ladders: list[Ladder]
    no_of_pieces: int