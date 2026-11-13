from config import LEADERBOARD_SIZE
from leaderboard import load_scores, add_score, insertion_sort, linear_search, binary_search
from terminal_ui import play, clear, curses


def show_leaderboard():
    scores = insertion_sort(load_scores())
    print("\n=== LEADERBOARD ===")
    if not scores:
        print("No scores yet.")
    for rank, s in enumerate(scores[:LEADERBOARD_SIZE], 1):
        print(f"{rank:>2}. {s['name']:<12} {s['score']}")
    input("\nPress Enter to go back...")


def search_menu():
    scores = insertion_sort(load_scores())
    print("\n=== SEARCH ===")
    print("1. Find a player by name (linear search)")
    print("2. Find a score (binary search)")
    choice = input("> ").strip()

    if choice == "1":
        name = input("Name: ").strip()
        i = linear_search(scores, name)
        if i == -1:
            print(f"'{name}' was not found.")
        else:
            print(f"Found {scores[i]['name']}: best score {scores[i]['score']} (rank {i + 1})")
    elif choice == "2":
        text = input("Score: ").strip()
        i = binary_search(scores, int(text)) if text.isdigit() else None
        if i is None:
            print("Please type a number.")
        elif i == -1:
            print(f"No one has a score of {text}.")
        else:
            print(f"Score {text} belongs to {scores[i]['name']} (rank {i + 1})")

    input("\nPress Enter to go back...")


def game_over(score):
    saved = False
    while True:
        print(f"\n*** GAME OVER ***  Final score: {score}")
        print("[S] Save score   [V] View scores   [R] Restart   [Q] Quit")
        choice = input("> ").strip().lower()
        if choice == "s" and saved:
            print("Score already saved.")
        elif choice == "s":
            name = input("Enter your name: ").strip()
            if name:
                add_score(name[:12], score)
                saved = True
                print("Score saved!")
        elif choice == "v":
            show_leaderboard()
        elif choice == "r":
            return "restart"
        elif choice == "q":
            return "quit"


def main():
    while True:
        clear()
        print("=========================")
        print("      METEOR ESCAPE      ")
        print("=========================")
        print("Mode:", "real-time" if curses else "turn-based (pip install windows-curses for real-time)")
        print("1. Play")
        print("2. Leaderboard")
        print("3. Search scores")
        print("4. Quit")
        choice = input("> ").strip().lower()

        if choice == "1":
            result = game_over(play())
            while result == "restart":
                result = game_over(play())
            if result == "quit":
                print("Thanks for playing!")
                break
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            search_menu()
        elif choice in ("4", "q"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
