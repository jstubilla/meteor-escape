import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import BOARD_WIDTH, BOARD_HEIGHT, START_LIVES
from player import create_player, move_player
from meteors import move_meteors, check_collision
from scoring import add_points
from game import new_game, update
from leaderboard import (insertion_sort, linear_search, binary_search,
                         save_scores, load_scores, add_score)


class TestPlayer(unittest.TestCase):
    def test_player_stays_inside_board(self):
        player = create_player()
        for _ in range(BOARD_WIDTH + 5):
            move_player(player, "a")
        self.assertEqual(player["x"], 0)
        for _ in range(BOARD_WIDTH + 5):
            move_player(player, "d")
        self.assertEqual(player["x"], BOARD_WIDTH - 1)


class TestMeteors(unittest.TestCase):
    def test_collision_loses_only_one_life(self):
        player, game, meteors = new_game()
        meteors.append({"x": player["x"], "y": player["y"] - 1})
        meteors.append({"x": player["x"], "y": player["y"] - 1})
        update(player, game, meteors, "")
        self.assertEqual(player["lives"], START_LIVES - 1)

    def test_collision_removes_meteor(self):
        player = create_player()
        meteors = [{"x": player["x"], "y": player["y"]}]
        self.assertTrue(check_collision(meteors, player))
        self.assertEqual(meteors, [])

    def test_meteor_passes_bottom(self):
        meteors = [{"x": 3, "y": BOARD_HEIGHT - 1}]
        passed = move_meteors(meteors)
        self.assertEqual(passed, 1)
        self.assertEqual(meteors, [])


class TestScoring(unittest.TestCase):
    def test_points_and_level(self):
        game = {"score": 0, "level": 1}
        add_points(game, 4)
        self.assertEqual(game["level"], 1)
        add_points(game, 1)
        self.assertEqual(game["score"], 50)
        self.assertEqual(game["level"], 2)


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.scores = insertion_sort([
            {"name": "Ana", "score": 30},
            {"name": "Ben", "score": 90},
            {"name": "Cy", "score": 60},
        ])

    def test_sort_highest_first(self):
        self.assertEqual([s["score"] for s in self.scores], [90, 60, 30])

    def test_linear_search(self):
        self.assertEqual(linear_search(self.scores, "cy"), 1)
        self.assertEqual(linear_search(self.scores, "Zed"), -1)

    def test_binary_search(self):
        self.assertEqual(binary_search(self.scores, 90), 0)
        self.assertEqual(binary_search(self.scores, 30), 2)
        self.assertEqual(binary_search(self.scores, 45), -1)
        self.assertEqual(binary_search([], 10), -1)

    def test_save_and_reload(self):
        path = os.path.join(tempfile.mkdtemp(), "scores.json")
        save_scores(self.scores, path)
        self.assertEqual(load_scores(path), self.scores)
        add_score("Dee", 75, path)
        self.assertEqual([s["name"] for s in load_scores(path)], ["Ben", "Dee", "Cy", "Ana"])

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(load_scores("does_not_exist.json"), [])


class TestRestart(unittest.TestCase):
    def test_new_game_resets_everything(self):
        player, game, meteors = new_game()
        player["lives"] = 0
        game["score"] = 120
        player, game, meteors = new_game()
        self.assertEqual(player["lives"], START_LIVES)
        self.assertEqual(game["score"], 0)
        self.assertEqual(meteors, [])


if __name__ == "__main__":
    unittest.main()
