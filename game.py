# game.py - game rules: one game update, and the board
from config import BOARD_WIDTH, BOARD_HEIGHT, PLAYER_CHAR, METEOR_CHAR, EMPTY_CHAR
from player import create_player, move_player
from meteors import spawn_meteor, move_meteors, check_collision
from scoring import add_points, meteors_per_update


def new_game():
    player = create_player()            # dictionary
    game = {"score": 0, "level": 1}     # dictionary
    meteors = []                        # list
    return player, game, meteors


def build_board(player, meteors):
    # 2D list: board[row][column]
    board = [[EMPTY_CHAR] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    for m in meteors:
        board[m["y"]][m["x"]] = METEOR_CHAR
    board[player["y"]][player["x"]] = PLAYER_CHAR
    return board


def move_step(player, meteors, key):
    """Move the ship. Returns True if it moved into a meteor."""
    move_player(player, key)
    return check_collision(meteors, player)


def fall_step(player, game, meteors):
    """Spawn meteors, move them down, score the ones that passed. Returns True on a hit."""
    for _ in range(meteors_per_update(game["level"])):
        spawn_meteor(meteors)
    avoided = move_meteors(meteors)
    hit = check_collision(meteors, player)
    add_points(game, avoided)
    return hit


def lose_life(player):
    player["lives"] = max(0, player["lives"] - 1)


def update(player, game, meteors, key):
    """One full turn: move, then fall. Only one life is lost per update."""
    hit_moving = move_step(player, meteors, key)
    hit_falling = fall_step(player, game, meteors)
    if hit_moving or hit_falling:
        lose_life(player)
