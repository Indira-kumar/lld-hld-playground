from random import randint

from .models import *

def create_game() -> Game:
    no_of_players = input("Enter number of players: ")
    while (no_of_players < 2):
        print("Number of players can't be less than 2.")
        no_of_players = input("Enter number of players: ")
    no_of_pieces = input("Enter number of pieces: ")
    while (no_of_pieces < 1):
        print("Number of pieces can't be less than 1.")
        no_of_pieces = input("Enter number of pieces: ")
    players = []
    for _ in no_of_players:
        name = input("Enter your name: ")
        color = input("Enter your color: ")
        age = input("Enter your age: ")
        gender = input("Enter your gender: ")
        player = Player(name=name, color=color, age=age, gender=gender)
        players.append(player)

    dims = input("Enter the dimension of the board: ")
    while (dims < 5):
        print("Number of dimensions can't be less than 5.")
        dims = input("Enter the dimension of the board: ")
    board = Board(n=dims)
    pieces = []
    for i, player in enumerate(players):
        for j in range(no_of_pieces):
            piece = Piece(id=(i*no_of_players + j), color=player.color, position=Position(-1,-1), player=player)
            pieces.append(piece)
    print("Pieces Initialized")

    no_of_snakes = randint(1, dims)
    no_of_frogs = randint(1, dims)
    no_of_ladders = randint(1, dims)
    snakes = []
    for i in range(no_of_snakes):
        start_pos = Position(x= randint(1, dims), y=randint(1, dims))
        end_pos = Position(x= randint(1, dims), y=randint(1, start_pos.y))
        snakes.append(Snake(start_pos=start_pos, end_pos=end_pos))
    frogs = []
    for i in range(no_of_frogs):
        start_pos = Position(x= randint(1, dims-1), y=randint(1, dims-1))
        end_pos = Position(x= randint(1, dims), y=randint(start_pos.y, dims))
        frogs.append(Frog(start_pos=start_pos, end_pos=end_pos))
    ladders = []
    for i in range(no_of_ladders):
        start_pos = Position(x= randint(1, dims-1), y=randint(1, dims-1))
        end_pos = Position(x= randint(1, dims-1), y=randint(start_pos.y, dims))
        ladders.append(Ladder(start_pos=start_pos, end_pos=end_pos))

    return Game(players=players, pieces=pieces, board=board, snakes=snakes, frogs=frogs, ladders=ladders, no_of_pieces=no_of_pieces)


def play_game(game:Game):
    pass


def __main__():
    game = create_game()
    play_game(game)