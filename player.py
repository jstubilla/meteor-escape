from config import BOARD_WIDTH, BOARD_HEIGHT, START_LIVES


def create_player():
    return {"x": BOARD_WIDTH // 2, "y": BOARD_HEIGHT - 1, "lives": START_LIVES}


def move_player(player, key):
    if key == "a":
        player["x"] = max(0, player["x"] - 1)
    elif key == "d":
        player["x"] = min(BOARD_WIDTH - 1, player["x"] + 1)
