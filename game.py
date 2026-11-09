# game.py - main game loop and board drawing
import os
from config import BOARD_WIDTH, BOARD_HEIGHT, PLAYER_CHAR, METEOR_CHAR, EMPTY_CHAR
from player import create_player, move_player
from meteors import spawn_meteor, move_meteors, check_collision
from scoring import add_points


def build_board(player, meteors):
    # 2D list: board[row][column]
    board = [[EMPTY_CHAR] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    for m in meteors:
        board[m["y"]][m["x"]] = METEOR_CHAR
    board[player["y"]][player["x"]] = PLAYER_CHAR
    return board


def draw(board, player, game):
    os.system("cls" if os.name == "nt" else "clear")
    print("=== METEOR ESCAPE ===")
    print(f"Score: {game['score']}   Lives: {player['lives']}   Level: {game['level']}")
    for row in board:
        print(" ".join(row))
    print("[a] left  [d] right  [Enter] stay  [q] quit")


def update(player, game, meteors, key):
    """One game update (1 turn): move, spawn, fall, collide, score."""
    move_player(player, key)
    for _ in range(game["level"]):      # higher level -> more meteors per turn
        spawn_meteor(meteors)
    avoided = move_meteors(meteors)
    if check_collision(meteors, player):
        player["lives"] -= 1            # only one life lost per update
    add_points(game, avoided)


def run():
    while True:
        play_one_game()
        again = input("\n[R] restart  [Q] quit\n> ").strip().lower()
        if again != "r":
            print("Thanks for playing!")
            break


def play_one_game():
    player = create_player()
    game = {"score": 0, "level": 1}     # dictionary for game info
    meteors = []                        # list of active meteors

    while player["lives"] > 0:
        draw(build_board(player, meteors), player, game)
        key = input("> ").strip().lower()
        if key == "q":
            break
        update(player, game, meteors, key)

    draw(build_board(player, meteors), player, game)
    print(f"\nGAME OVER - Final score: {game['score']}")
