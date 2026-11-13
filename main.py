# main.py - start menu, game-over menu, leaderboard and search
from config import LEADERBOARD_SIZE
from leaderboard import load_scores, add_score, insertion_sort, linear_search, binary_search
from terminal_ui import play, clear, HAS_CURSES


def show_leaderboard():
    scores = insertion_sort(load_scores())
    print("\n=== LEADERBOARD ===")
    if not scores:
        print("No scores yet.")
    for rank, record in enumerate(scores[:LEADERBOARD_SIZE], start=1):
        print(f"{rank:>2}. {record['name']:<12} {record['score']}")
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
        try:
            target = int(input("Score: ").strip())
        except ValueError:
            print("Please type a number.")
        else:
            i = binary_search(scores, target)
            if i == -1:
                print(f"No one has a score of {target}.")
            else:
                print(f"Score {target} belongs to {scores[i]['name']} (rank {i + 1})")
    input("\nPress Enter to go back...")


def game_over(score):
    print(f"\n*** GAME OVER ***  Final score: {score}")
    name = input("Enter your name to save your score (or press Enter to skip): ").strip()
    if name:
        add_score(name[:12], score)
        print("Score saved!")
    return input("[R] Restart   [Enter] Main menu\n> ").strip().lower() == "r"


def main():
    while True:
        clear()
        print("=========================")
        print("      METEOR ESCAPE      ")
        print("=========================")
        print("Mode:", "real-time" if HAS_CURSES else "turn-based (pip install windows-curses for real-time)")
        print("1. Play")
        print("2. Leaderboard")
        print("3. Search scores")
        print("4. Quit")
        choice = input("> ").strip().lower()
        if choice == "1":
            while game_over(play()):    # R restarts right away
                pass
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            search_menu()
        elif choice in ("4", "q"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
