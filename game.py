from config import BOARD_WIDTH, BOARD_HEIGHT, PLAYER_CHAR, METEOR_CHAR, EMPTY_CHAR
from player import create_player, move_player
from meteors import spawn_meteor, move_meteors, check_collision
from scoring import add_points, spawn_count


def new_game():
    return create_player(), {"score": 0, "level": 1}, []


def build_board(player, meteors):
    board = [[EMPTY_CHAR] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    for m in meteors:
        board[m["y"]][m["x"]] = METEOR_CHAR
    board[player["y"]][player["x"]] = PLAYER_CHAR
    return board


def move_step(player, meteors, key):
    move_player(player, key)
    return check_collision(meteors, player)


def fall_step(player, game, meteors):
    for _ in range(spawn_count(game["level"])):
        spawn_meteor(meteors)
    add_points(game, move_meteors(meteors))
    return check_collision(meteors, player)


def update(player, game, meteors, key):
    moved = move_step(player, meteors, key)
    fell = fall_step(player, game, meteors)
    if moved or fell:
        player["lives"] -= 1
