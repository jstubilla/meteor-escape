from config import POINTS_PER_METEOR, POINTS_PER_LEVEL


def add_points(game, avoided):
    game["score"] += avoided * POINTS_PER_METEOR
    game["level"] = game["score"] // POINTS_PER_LEVEL + 1


def spawn_count(level):
    return min(1 + (level - 1) // 2, 3)


def tick_delay(level):
    return max(0.12, 0.45 - 0.05 * (level - 1))
