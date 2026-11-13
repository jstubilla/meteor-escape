import json
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "data" / "high_scores.json"


def load_scores(path=SCORES_FILE):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_scores(scores, path=SCORES_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scores, indent=2), encoding="utf-8")


def insertion_sort(scores):
    out = list(scores)
    for i in range(1, len(out)):
        cur = out[i]
        j = i - 1
        while j >= 0 and out[j]["score"] < cur["score"]:
            out[j + 1] = out[j]
            j -= 1
        out[j + 1] = cur
    return out


def linear_search(scores, name):
    for i, s in enumerate(scores):
        if s["name"].lower() == name.lower():
            return i
    return -1


def binary_search(scores, target):
    lo, hi = 0, len(scores) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = scores[mid]["score"]
        if val == target:
            return mid
        if val > target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def add_score(name, score, path=SCORES_FILE):
    scores = insertion_sort(load_scores(path) + [{"name": name, "score": score}])
    save_scores(scores, path)
    return scores
