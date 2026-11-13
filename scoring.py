# scoring.py - points, level and difficulty
from config import POINTS_PER_METEOR, POINTS_PER_LEVEL


def add_points(game, meteors_avoided):
    game["score"] += meteors_avoided * POINTS_PER_METEOR
    game["level"] = game["score"] // POINTS_PER_LEVEL + 1   # level up every 50 points


def meteors_per_update(level):
    # more meteors at higher levels (1, 1, 2, 2, 3, ... max 3)
    return min(1 + (level - 1) // 2, 3)


def seconds_per_update(level):
    # faster meteors at higher levels (real-time mode only)
    return max(0.12, 0.45 - 0.05 * (level - 1))
