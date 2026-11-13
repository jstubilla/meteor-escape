import random
from config import BOARD_WIDTH, BOARD_HEIGHT


def spawn_meteor(meteors):
    meteors.append({"x": random.randrange(BOARD_WIDTH), "y": 0})


def move_meteors(meteors):
    for m in meteors:
        m["y"] += 1
    kept = [m for m in meteors if m["y"] < BOARD_HEIGHT]
    passed = len(meteors) - len(kept)
    meteors[:] = kept
    return passed


def check_collision(meteors, player):
    kept = [m for m in meteors if (m["x"], m["y"]) != (player["x"], player["y"])]
    hit = len(kept) < len(meteors)
    meteors[:] = kept
    return hit
