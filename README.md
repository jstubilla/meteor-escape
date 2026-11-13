# Meteor Escape

A spaceship survival game in Python. Move left and right to dodge falling meteors.

Play online: https://jstubilla.github.io/meteor-escape/

## How to run

Requirements: Python 3.8 or newer.

```
pip install -r requirements.txt
python main.py
```

On Mac or Linux, use `python3 main.py`. Without `windows-curses` on Windows, the game still runs, in turn-based mode.

## Controls

| Key | Action |
|---|---|
| A / Left Arrow | Move left |
| D / Right Arrow | Move right |
| Q | Quit the game |
| R | Restart after game over |

## Rules

- You start with 3 lives.
- Each meteor you avoid is worth 10 points.
- The level goes up every 50 points. Higher levels have more and faster meteors.
- The game ends when your lives reach zero. You can then save your score.

## Tests

```
python -m unittest discover -s tests
```
