# player.py - player data (dictionary) and movement
from config import BOARD_WIDTH, BOARD_HEIGHT, START_LIVES


def create_player():
    # Dictionary: stores player info by name (key -> value)
    return {
        "x": BOARD_WIDTH // 2,
        "y": BOARD_HEIGHT - 1,   # spaceship stays on the bottom row
        "lives": START_LIVES,
    }


def move_player(player, key):
    if key == "a" and player["x"] > 0:
        player["x"] -= 1
    elif key == "d" and player["x"] < BOARD_WIDTH - 1:
        player["x"] += 1
    # the two checks above keep the ship inside the board
