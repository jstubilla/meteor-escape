# terminal_ui.py - shows the game in the terminal (real-time with curses, or turn-based)
import os
import time
from game import new_game, build_board, move_step, fall_step, update, lose_life
from scoring import seconds_per_update

try:
    import curses                       # on Windows: pip install windows-curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def status_line(player, game):
    return f"Score: {game['score']}   Lives: {player['lives']}   Level: {game['level']}"


# ---------- turn-based version (works everywhere) ----------

def play_turn_based():
    player, game, meteors = new_game()
    while player["lives"] > 0:
        clear()
        print("=== METEOR ESCAPE ===")
        print(status_line(player, game))
        for row in build_board(player, meteors):
            print(" ".join(row))
        print("[a] left  [d] right  [Enter] stay  [q] quit")
        key = input("> ").strip().lower()
        if key == "q":
            break
        update(player, game, meteors, key)
    return game["score"]


# ---------- real-time version (curses) ----------

KEYS = {ord("a"): "a", ord("A"): "a", ord("d"): "d", ord("D"): "d"}


def _realtime_loop(screen):
    curses.curs_set(0)                  # hide the cursor
    screen.nodelay(True)                # getch() does not wait for a key
    player, game, meteors = new_game()
    next_fall = time.time() + seconds_per_update(game["level"])

    while player["lives"] > 0:
        # 1. input: read every key pressed since last frame
        key = screen.getch()
        while key != -1:
            if key in (ord("q"), ord("Q")):
                return game["score"]
            move = KEYS.get(key)
            if key == curses.KEY_LEFT:
                move = "a"
            elif key == curses.KEY_RIGHT:
                move = "d"
            if move and move_step(player, meteors, move):
                lose_life(player)
            key = screen.getch()

        # 2. update: meteors fall on a timer (faster at higher levels)
        if time.time() >= next_fall:
            if fall_step(player, game, meteors):
                lose_life(player)
            next_fall = time.time() + seconds_per_update(game["level"])

        # 3. render
        screen.erase()
        try:
            screen.addstr(0, 0, "=== METEOR ESCAPE ===")
            screen.addstr(1, 0, status_line(player, game))
            for y, row in enumerate(build_board(player, meteors)):
                screen.addstr(y + 2, 0, " ".join(row))
            screen.addstr(y + 3, 0, "A/Left  D/Right  Q quit")
        except curses.error:
            screen.erase()
            try:
                screen.addstr(0, 0, "Make the window bigger!")
            except curses.error:
                pass
        screen.refresh()
        time.sleep(0.02)

    return game["score"]


def play_realtime():
    return curses.wrapper(_realtime_loop)


def play():
    """Play one game and return the final score."""
    return play_realtime() if HAS_CURSES else play_turn_based()
