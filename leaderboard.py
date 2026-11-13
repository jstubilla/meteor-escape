# leaderboard.py - save, load, sort and search high scores
import json
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "data" / "high_scores.json"


def load_scores(path=SCORES_FILE):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []                       # no file yet, or broken file -> empty list


def save_scores(scores, path=SCORES_FILE):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def insertion_sort(scores):
    """Sort records from highest to lowest score. O(n^2) worst case."""
    result = list(scores)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        # shift lower scores one place to the right
        while j >= 0 and result[j]["score"] < current["score"]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def linear_search(scores, name):
    """Check names one by one. Returns the index, or -1 if not found. O(n)"""
    for i in range(len(scores)):
        if scores[i]["name"].lower() == name.lower():
            return i
    return -1


def binary_search(scores, target):
    """Find a score in a list sorted high -> low. Returns the index, or -1. O(log n)"""
    low, high = 0, len(scores) - 1
    while low <= high:
        mid = (low + high) // 2
        value = scores[mid]["score"]
        if value == target:
            return mid
        elif value > target:            # list goes high -> low, so look right
            low = mid + 1
        else:
            high = mid - 1
    return -1


def add_score(name, score, path=SCORES_FILE):
    scores = load_scores(path)
    scores.append({"name": name, "score": score})
    scores = insertion_sort(scores)
    save_scores(scores, path)
    return scores
