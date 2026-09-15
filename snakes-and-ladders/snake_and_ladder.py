from random import randint

from .models import *
from .dice_strategy import DefaultDiceStrategy

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
    pieces = {}
    for i, player in enumerate(players):
        for j in range(no_of_pieces):
            piece = Piece(id=(i*no_of_players + j), color=player.color, position=Position(-1,-1), player=player)
            pieces[player.name] = [piece] if not pieces[player.name] else pieces[player.name].append(piece)
    print("\nPieces Initialized")

    no_of_snakes = randint(1, dims)
    no_of_frogs = randint(1, dims)
    no_of_ladders = randint(1, dims)
    snakes = []
    special_chars = {}
    cnt = 0
    while(cnt < no_of_snakes):
        start_pos = Position(x= randint(1, dims), y=randint(1, dims))
        end_pos = Position(x= randint(1, dims), y=randint(1, start_pos.y))
        snake = Snake(start_pos=start_pos, end_pos=end_pos)
        if not special_chars[start_pos.x][start_pos.y]:
            snakes.append(snake)
            special_chars[start_pos.x][start_pos.y] = snake
            cnt += 1
        else:
            continue
    frogs = []
    cnt = 0
    while(cnt < no_of_frogs):
        start_pos = Position(x= randint(1, dims-1), y=randint(1, dims-1))
        end_pos = Position(x= randint(1, dims), y=randint(start_pos.y, dims))
        frog = Frog(start_pos=start_pos, end_pos=end_pos)
        if not special_chars[start_pos.x][start_pos.y]:
            frogs.append(frog)
            special_chars[start_pos.x][start_pos.y] = frog
            cnt += 1
        else:
            continue
    ladders = []
    cnt = 0
    while(cnt < no_of_ladders):
        start_pos = Position(x= randint(1, dims-1), y=randint(1, dims-1))
        end_pos = Position(x= randint(1, dims-1), y=randint(start_pos.y, dims))
        ladder = Ladder(start_pos=start_pos, end_pos=end_pos)
        if not special_chars[start_pos.x][start_pos.y]:
            ladders.append(ladder)
            special_chars[start_pos.x][start_pos.y] = ladder
            cnt += 1
        else:
            continue

    board = Board(n=dims, special_chars=special_chars)

    return Game(players=players, pieces=pieces, board=board, snakes=snakes, frogs=frogs, ladders=ladders, no_of_pieces=no_of_pieces)

def _get_valid_count_helper(var_name: str, min_count: int):
    var = input(f"\nEnter the {var_name}: ")
    while (var < min_count):
        print(f"\nNumber of {var_name} can't be less than {min_count}.")
        var = input(f"\nEnter the {var_name}: ")
    return var

def play_game(game:Game):
    print("\nGame Started")
    dice = DefaultDiceStrategy()
    game_won = False
    while(not game_won):
        for i in game.players:
            number = dice.roll_dice()
            print("\nRolling the dice for: ", i.name)
            print(f"\nYou got: {number}")
            choice = input("\nChoose which piece to move: ", game.pieces[i.name])
            move_piece(game, game.pieces[i.name][choice], number)
            game_won = _is_game_won()


def move_piece(game: Game, piece: Piece, move_count: int):
    dim = game.board.n
    curr_pos = piece.position
    game.board.positions[curr_pos.x][curr_pos.y].remove(piece)
    x = move_count % dim
    y = move_count // dim
    if game.board.special_chars[x][y]:
        x = game.board.special_chars[x][y].end_position.x
        y = game.board.special_chars[x][y].end_position.y

    piece.position = Position(x, y)
    game.board.positions[x][y].append(piece)
    print("\nPiece moved")

def _is_game_won() -> bool:
    pass


def __main__():
    game = create_game()
    play_game(game)