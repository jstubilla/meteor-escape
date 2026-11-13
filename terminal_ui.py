import os
import time
from game import new_game, build_board, move_step, fall_step, update
from scoring import tick_delay

try:
    import curses
except ImportError:
    curses = None


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def status(player, game):
    return f"Score: {game['score']}   Lives: {player['lives']}   Level: {game['level']}"


def play_turn_based():
    player, game, meteors = new_game()
    while player["lives"] > 0:
        clear()
        print("=== METEOR ESCAPE ===")
        print(status(player, game))
        for row in build_board(player, meteors):
            print(" ".join(row))
        print("[a] left  [d] right  [Enter] stay  [q] quit")
        key = input("> ").strip().lower()
        if key == "q":
            break
        update(player, game, meteors, key)
    return game["score"]


def realtime(screen):
    curses.curs_set(0)
    screen.nodelay(True)
    keys = {ord("a"): "a", ord("A"): "a", ord("d"): "d", ord("D"): "d",
            curses.KEY_LEFT: "a", curses.KEY_RIGHT: "d"}
    player, game, meteors = new_game()
    tick = time.time() + tick_delay(game["level"])

    while player["lives"] > 0:
        key = screen.getch()
        while key != -1 and player["lives"] > 0:
            if key in (ord("q"), ord("Q")):
                return game["score"]
            if key in keys and move_step(player, meteors, keys[key]):
                player["lives"] -= 1
            key = screen.getch()

        if player["lives"] > 0 and time.time() >= tick:
            if fall_step(player, game, meteors):
                player["lives"] -= 1
            tick = time.time() + tick_delay(game["level"])

        lines = ["=== METEOR ESCAPE ===", status(player, game)]
        lines += [" ".join(row) for row in build_board(player, meteors)]
        lines.append("A/Left  D/Right  Q quit")
        screen.erase()
        try:
            for y, line in enumerate(lines):
                screen.addstr(y, 0, line)
        except curses.error:
            pass
        screen.refresh()
        time.sleep(0.02)

    return game["score"]


def play():
    return curses.wrapper(realtime) if curses else play_turn_based()
