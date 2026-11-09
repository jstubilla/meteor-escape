# scoring.py - points and level
from config import POINTS_PER_METEOR, POINTS_PER_LEVEL


def add_points(game, meteors_avoided):
    game["score"] += meteors_avoided * POINTS_PER_METEOR
    game["level"] = game["score"] // POINTS_PER_LEVEL + 1   # level up every 50 points
