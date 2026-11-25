
import random
from pathlib import Path

WORD_FILE = Path(__file__).with_name("words.txt")
MAX_MISTAKES = 6

HANGMAN_STAGES = [
    """
     +---+
         |
         |
         |
        ===
    """,
    """
     +---+
     O   |
         |
         |
        ===
    """,
    """
     +---+
     O   |
     |   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===
    """
]


def load_words():
    try:
        words = [
            word.strip().lower()
            for word in WORD_FILE.read_text().splitlines()
            if word.strip().isalpha() and len(word.strip()) >= 4
        ]
    except FileNotFoundError:
        words = []

    if not words:
        print("Word list not found. Using default words.")
        words = ["python", "cloud", "server", "docker"]

    return words


def display_game(secret_word, guessed_letters, wrong_guesses):

    print(HANGMAN_STAGES[len(wrong_guesses)])

    masked_word = " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:", masked_word)
    print("Wrong guesses:", len(wrong_guesses), "/", MAX_MISTAKES)
    print("Guessed letters:", ", ".join(sorted(guessed_letters | wrong_guesses)))
    print("Remaining chances:", MAX_MISTAKES - len(wrong_guesses))


def play_game():

    secret_word = random.choice(load_words())

    guessed_letters = set()
    wrong_guesses = set()

    print("\n========== HANGMAN ==========")
    print("Guess the hidden word!")

    while len(wrong_guesses) < MAX_MISTAKES:

        display_game(secret_word, guessed_letters, wrong_guesses)

        if all(letter in guessed_letters for letter in secret_word):
            print("\n*** YOU WIN! ***")
            print("The word was:", secret_word.upper())
            return

        guess = input("\nEnter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one alphabetic letter.")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("You already guessed that letter!")
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
            print("Correct guess!")
        else:
            wrong_guesses.add(guess)
            print("Incorrect guess!")

    display_game(secret_word, guessed_letters, wrong_guesses)

    print("\n*** GAME OVER ***")
    print("The correct word was:", secret_word.upper())


def main():

    while True:
        play_game()

        again = input("\nPlay again? (y/n): ").strip().lower()

        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
