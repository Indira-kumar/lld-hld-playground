from random import randint

from .models import *

def create_game() -> Game:
    no_of_players = _get_valid_count_helper('no. of players', 2)
    no_of_pieces = _get_valid_count_helper('no. of pieces', 1)
    players = []
    for _ in no_of_players:
        name = input("\n\nEnter your name: ")
        color = input("\nEnter your color: ")
        age = input("\nEnter your age: ")
        gender = input("\nEnter your gender: ")
        player = Player(name=name, color=color, age=age, gender=gender)
        players.append(player)

    dims = _get_valid_count_helper('dimension of board', 5)
    board = Board(n=dims)
    pieces = []
    for i, player in enumerate(players):
        for j in range(no_of_pieces):
            piece = Piece(id=(i*no_of_players + j), color=player.color, position=Position(-1,-1), player=player)
            pieces.append(piece)
    print("\nPieces Initialized")

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

def _get_valid_count_helper(var_name: str, min_count: int):
    var = input(f"\nEnter the {var_name}: ")
    while (var < min_count):
        print(f"\nNumber of {var_name} can't be less than {min_count}.")
        var = input(f"\nEnter the {var_name}: ")
    return var

def play_game(game:Game):
    print("Game Started")


def __main__():
    game = create_game()
    play_game(game)