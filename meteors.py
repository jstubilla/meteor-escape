# meteors.py - meteor list, movement and collision detection
import random
from config import BOARD_WIDTH, BOARD_HEIGHT


def spawn_meteor(meteors):
    # List: each meteor is a small dictionary {"x": column, "y": row}
    meteors.append({"x": random.randint(0, BOARD_WIDTH - 1), "y": 0})


def move_meteors(meteors):
    """Move every meteor down one row. Returns how many passed the bottom."""
    passed = 0
    for meteor in meteors[:]:          # O(n) traversal (copy so we can remove safely)
        meteor["y"] += 1
        if meteor["y"] >= BOARD_HEIGHT:
            meteors.remove(meteor)
            passed += 1
    return passed


def check_collision(meteors, player):
    """Return True if any meteor is on the player's cell. Removes those meteors."""
    hit = False
    for meteor in meteors[:]:          # O(n) linear check
        if meteor["x"] == player["x"] and meteor["y"] == player["y"]:
            meteors.remove(meteor)
            hit = True
    return hit                         # caller removes only ONE life per update
