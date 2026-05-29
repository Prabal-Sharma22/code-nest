# """Mega Program: a 500-line Python utility suite.

# This file contains multiple small interactive tools and games.
# The goal is to provide a complete, well-structured Python script
# with strong input validation, clear functions, and a pleasant CLI.
# """
# from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple


MAX_GUESS_NUMBER = 100
DEFAULT_ATTEMPTS = 10
MIN_GUESS_NUMBER = 1
MAX_MENU_WIDTH = 72


def safe_input(
    prompt: str,
    validator: Callable[[str], bool],
    error_message: str,
    default: Optional[str] = None,
) -> str:
    """Ask the user for input until the response is valid."""
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        if validator(raw):
            return raw
        print(error_message)


def get_int_input(
    prompt: str,
    min_value: int,
    max_value: int,
    default: Optional[int] = None,
) -> int:
    """Read an integer from the user and enforce bounds."""
    def validator(value: str) -> bool:
        if not value.isdigit():
            return False
        numeric = int(value)
        return min_value <= numeric <= max_value

    message = f"Enter a number between {min_value} and {max_value}."
    if default is not None:
        message += f" Press Enter to use {default}."

    answer = safe_input(prompt, validator, message, default=str(default) if default else None)
    return int(answer)


def print_divider(title: str = "") -> None:
    """Print a divider line with an optional title."""
    if title:
        title_line = f" {title} "
        print(title_line.center(MAX_MENU_WIDTH, "="))
    else:
        print("=" * MAX_MENU_WIDTH)


def yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    """Ask the user a yes/no question."""
    options = " [y/n] "
    if default is True:
        options = " [Y/n] "
    elif default is False:
        options = " [y/N] "

    def validator(text: str) -> bool:
        lowercase = text.lower()
        return lowercase in {"y", "yes", "n", "no"}

    answer = safe_input(prompt + options, validator, "Please type yes or no.")
    normalized = answer.lower()
    if normalized in {"y", "yes"}:
        return True
    if normalized in {"n", "no"}:
        return False
    return default if default is not None else False


def choose_option(prompt: str, options: Sequence[str]) -> int:
    """Display a list of choices and return the selected index."""
    print(prompt)
    for count, option in enumerate(options, start=1):
        print(f"  {count}. {option}")
    print()
    message = f"Choose an option from 1 to {len(options)}."

    def validator(value: str) -> bool:
        return value.isdigit() and 1 <= int(value) <= len(options)

    answer = safe_input("Select option: ", validator, message)
    return int(answer) - 1


def pause() -> None:
    """Pause until the user presses Enter."""
    input("Press Enter to continue...")


def clear_screen() -> None:
    """Clear the screen in a gentle cross-platform way."""
    print("\n" * 3)


@dataclass
class ScoreRecord:
    player_name: str
    score: int
    attempts: int


class GuessingGame:
    """A simple number-guessing game with a score panel."""

    def __init__(self, max_number: int = MAX_GUESS_NUMBER, attempts: int = DEFAULT_ATTEMPTS, seed: Optional[int] = None) -> None:
        self.max_number = max(1, max_number)
        self.attempts = max(1, attempts)
        self.seed = seed
        self.secret_number = self._generate_secret()

    def _generate_secret(self) -> int:
        rng = random.Random(self.seed)
        return rng.randint(MIN_GUESS_NUMBER, self.max_number)

    def _feedback(self, guess: int) -> str:
        if guess == self.secret_number:
            return "correct"
        if guess < self.secret_number:
            return "low"
        return "high"

    def play(self) -> ScoreRecord:
        print_divider("Guessing Game")
        print(f"Guess a number between {MIN_GUESS_NUMBER} and {self.max_number}.")
        print(f"You have {self.attempts} attempts.")

        for attempt in range(1, self.attempts + 1):
            guess = get_int_input(f"Attempt {attempt}/{self.attempts}: ", MIN_GUESS_NUMBER, self.max_number)
            feedback = self._feedback(guess)
            if feedback == "correct":
                print(f"Nice work! You guessed the number in {attempt} attempts.")
                return ScoreRecord("Player", 100 - attempt, attempt)
            print("Too low." if feedback == "low" else "Too high.")
        print(f"Sorry, the correct number was {self.secret_number}.")
        return ScoreRecord("Player", 0, self.attempts)

    @staticmethod
    def summary(record: ScoreRecord) -> None:
        print_divider("Guessing Game Summary")
        print(f"Name: {record.player_name}")
        print(f"Attempts used: {record.attempts}")
        print(f"Score: {record.score}")


class WordScrambleGame:
    """A word scramble game that picks a word and asks the player to unscramble it."""

    WORD_LIST: List[str] = [
        "planet",
        "dragon",
        "picture",
        "holiday",
        "whisper",
        "silence",
        "journey",
        "network",
        "library",
        "tomato",
        "umbrella",
        "journal",
        "coffee",
        "battery",
        "diamond",
        "forecast",
        "gallery",
        "horizon",
        "island",
        "jungle",
        "kitchen",
        "lantern",
        "mystery",
        "nature",
        "ocean",
        "pyramid",
        "quantum",
        "rhythm",
        "sunlight",
        "treasure",
        "universe",
        "victory",
        "weather",
        "xylophone",
        "youngster",
        "zeppelin",
        "acoustic",
        "bicycle",
        "carnival",
        "dolphin",
        "elevator",
        "festival",
        "gardener",
        "healing",
        "illusion",
        "justice",
        "kingdom",
        "language",
        "memory",
        "nostalgia",
        "optimize",
        "passion",
        "question",
        "rainbow",
        "science",
        "texture",
        "valley",
        "whistle",
        "yesterday",
        "zealous",
        "antique",
        "balance",
        "creation",
        "delicate",
        "elephant",
        "familiar",
        "gentle",
        "harmony",
        "imagine",
        "justice",
        "kingpin",
        "liberty",
        "magnet",
        "nectar",
        "orchard",
        "platinum",
        "quality",
        "remedy",
        "sapphire",
        "tornado",
        "umbrella",
        "velocity",
        "wonder",
        "xenon",
        "yearbook",
        "zodiac",
        "adventure",
        "bravery",
        "crescent",
        "delight",
        "embrace",
        "friend",
        "gentleman",
        "horizon",
        "inspire",
        "junction",
        "kingdom",
        "legend",
        "magnify",
        "novelty",
        "overture",
        "precious",
        "radiant",
        "shelter",
        "triumph",
        "umbrella",
        "vintage",
        "whimsical",
        "yearning",
        "zephyr",
    ]

    def __init__(self, rounds: int = 5) -> None:
        self.rounds = max(1, rounds)
        self.score = 0

    @staticmethod
    def scramble(word: str) -> str:
        letters = list(word)
        random.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled == word:
            random.shuffle(letters)
            scrambled = "".join(letters)
        return scrambled

    def play(self) -> None:
        print_divider("Word Scramble")
        print("Unscramble as many words as you can.")
        print(f"Rounds: {self.rounds}")
        for round_number in range(1, self.rounds + 1):
            word = random.choice(self.WORD_LIST)
            scrambled = self.scramble(word)
            print(f"Round {round_number}: {scrambled}")
            guess = input("Your unscrambled word: ").strip().lower()
            if guess == word:
                print("Correct!")
                self.score += 1
            else:
                print(f"Wrong. The answer was {word}.")
        print_divider("Scramble Score")
        print(f"You solved {self.score}/{self.rounds} words.")


class MathQuiz:
    """A short math quiz with multiple choice and numeric answers."""

    QUESTIONS: List[Tuple[str, str, float]] = [
        ("What is 7 + 6?", "13", 0.0),
        ("What is 8 * 7?", "56", 0.0),
        ("What is 45 / 9?", "5", 0.0),
        ("What is 12 squared?", "144", 0.0),
        ("What is 100 minus 37?", "63", 0.0),
        ("What is the square root of 81?", "9", 0.0),
        ("What is 5 cubed?", "125", 0.0),
        ("What is 15% of 200?", "30", 0.0),
        ("What is 3.5 + 2.4?", "5.9", 0.01),
        ("What is 9 * 9?", "81", 0.0),
        ("What is 14 + 28?", "42", 0.0),
        ("What is 40 / 8?", "5", 0.0),
        ("What is 6 * 12?", "72", 0.0),
        ("What is 99 minus 17?", "82", 0.0),
        ("What is 4 squared plus 10?", "26", 0.0),
        ("What is 3 times 11?", "33", 0.0),
        ("What is 60 divided by 12?", "5", 0.0),
        ("What is 18 + 24?", "42", 0.0),
        ("What is 7 times 8?", "56", 0.0),
        ("What is 100 / 25?", "4", 0.0),
    ]

    def __init__(self, questions: Optional[Sequence[Tuple[str, str, float]]] = None) -> None:
        self.questions = list(questions or self.QUESTIONS)
        self.correct_count = 0
        self.attempted = 0

    def _check_answer(self, answer: str, correct: str, tolerance: float) -> bool:
        if tolerance == 0.0:
            return answer.strip() == correct
        try:
            guess_value = float(answer)
            correct_value = float(correct)
        except ValueError:
            return False
        return abs(guess_value - correct_value) <= tolerance

    def play(self) -> None:
        print_divider("Math Quiz")
        random.shuffle(self.questions)
        for question, correct, tolerance in self.questions[:8]:
            response = input(f"{question} ")
            if self._check_answer(response, correct, tolerance):
                print("Correct!")
                self.correct_count += 1
            else:
                print(f"Incorrect. The answer was {correct}.")
            self.attempted += 1
        print_divider("Quiz Results")
        print(f"Correct: {self.correct_count}/{self.attempted}")


class TicTacToe:
    """A classic Tic Tac Toe game with a simple AI opponent."""

    def __init__(self) -> None:
        self.board = [" "] * 9
        self.current = "X"

    def display(self) -> None:
        print_divider("Tic Tac Toe")
        rows = [self.board[i:i + 3] for i in range(0, 9, 3)]
        for row in rows:
            print(" | ".join(row))
            print("---------")

    def available_moves(self) -> List[int]:
        return [index for index, value in enumerate(self.board) if value == " "]

    def _winning_line(self) -> Optional[str]:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        return None

    def _is_draw(self) -> bool:
        return all(space != " " for space in self.board) and self._winning_line() is None

    def _player_move(self) -> None:
        print("Select a cell from 1 to 9.")
        move = get_int_input("Your move: ", 1, 9)
        if self.board[move - 1] != " ":
            print("That space is already taken.")
            return self._player_move()
        self.board[move - 1] = "X"

    def _ai_move(self) -> None:
        for index in self.available_moves():
            self.board[index] = "O"
            if self._winning_line() == "O":
                return
            self.board[index] = " "
        for index in self.available_moves():
            self.board[index] = "X"
            if self._winning_line() == "X":
                self.board[index] = "O"
                return
            self.board[index] = " "
        for preferred in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
            if preferred in self.available_moves():
                self.board[preferred] = "O"
                return

    def play(self) -> None:
        print_divider("Tic Tac Toe")
        while True:
            self.display()
            self._player_move()
            winner = self._winning_line()
            if winner or self._is_draw():
                break
            self._ai_move()
            winner = self._winning_line()
            if winner or self._is_draw():
                break
        self.display()
        if winner:
            print(f"{winner} wins!")
        else:
            print("It's a draw.")


class AdventureGame:
    """A short text adventure with rooms, items, and simple commands."""

    ADVENTURE_MAP: Dict[str, Dict[str, object]] = {
        "entrance": {
            "description": "You stand at the entrance of an old stone castle.",
            "exits": {"north": "hall", "east": "garden"},
            "items": ["lantern"],
        },
        "hall": {
            "description": "A hall lined with portraits of ancient explorers.",
            "exits": {"south": "entrance", "east": "library"},
            "items": ["map"],
        },
        "garden": {
            "description": "A quiet garden with overgrown paths and fragrant flowers.",
            "exits": {"west": "entrance", "north": "tower"},
            "items": ["key"],
        },
        "library": {
            "description": "A dusty library filled with books on magic and travel.",
            "exits": {"west": "hall", "north": "study"},
            "items": ["spellbook"],
        },
        "study": {
            "description": "A small study with a secret drawer and a locked chest.",
            "exits": {"south": "library"},
            "items": [],
        },
        "tower": {
            "description": "The castle tower offers a view of the surrounding forest.",
            "exits": {"south": "garden"},
            "items": ["gemstone"],
        },
    }

    def __init__(self) -> None:
        self.location = "entrance"
        self.inventory: List[str] = []
        self.story_log: List[str] = []

    def _describe_location(self) -> None:
        room = self.ADVENTURE_MAP[self.location]
        print_divider(f"Location: {self.location.title()}")
        print(room["description"])
        print("Exits:")
        for direction in room["exits"]:
            print(f"  - {direction}")
        if room["items"]:
            print("Items here:")
            for item in room["items"]:
                print(f"  - {item}")

    def _move(self, direction: str) -> None:
        room = self.ADVENTURE_MAP[self.location]
        if direction not in room["exits"]:
            print("You can't go that way.")
            return
        self.location = room["exits"][direction]
        self.story_log.append(f"Moved {direction} to {self.location}.")

    def _take_item(self, item: str) -> None:
        room = self.ADVENTURE_MAP[self.location]
        if item not in room["items"]:
            print("There is nothing like that here.")
            return
        self.inventory.append(item)
        room["items"].remove(item)
        print(f"You picked up the {item}.")

    def _handle_command(self, command: str) -> bool:
        parts = command.lower().split()
        if not parts:
            return True
        if parts[0] in {"quit", "exit"}:
            return False
        if parts[0] in {"look", "l"}:
            self._describe_location()
            return True
        if parts[0] in {"inventory", "inv"}:
            print("Inventory:")
            for item in self.inventory:
                print(f"  - {item}")
            return True
        if parts[0] in {"go", "move"} and len(parts) > 1:
            self._move(parts[1])
            return True
        if parts[0] in {"take", "get"} and len(parts) > 1:
            self._take_item(parts[1])
            return True
        if parts[0] == "help":
            print("Commands: look, inventory, go <direction>, take <item>, quit")
            return True
        print("I don't understand that command.")
        return True

    def play(self) -> None:
        print_divider("Adventure Game")
        print("Find items and explore the castle.")
        self._describe_location()
        while True:
            command = input("What do you do? ")
            if not self._handle_command(command):
                break
            if self.location == "study" and "key" in self.inventory and "spellbook" in self.inventory:
                print("A hidden passage opens and you discover the secret treasure.")
                break
        print_divider("Adventure Complete")
        print("Thank you for playing the adventure.")


def run_guessing_game() -> None:
    print_divider("Start Guessing Game")
    game = GuessingGame(max_number=MAX_GUESS_NUMBER, attempts=DEFAULT_ATTEMPTS)
    record = game.play()
    GuessingGame.summary(record)
    pause()


def run_word_scramble() -> None:
    print_divider("Start Word Scramble")
    game = WordScrambleGame(rounds=6)
    game.play()
    pause()


def run_math_quiz() -> None:
    print_divider("Start Math Quiz")
    game = MathQuiz()
    game.play()
    pause()


def run_tic_tac_toe() -> None:
    print_divider("Start Tic Tac Toe")
    game = TicTacToe()
    game.play()
    pause()


def run_adventure_game() -> None:
    print_divider("Start Adventure Game")
    game = AdventureGame()
    game.play()
    pause()


def print_welcome_message() -> None:
    print_divider("Mega Program")
    print("Welcome to a multi-tool Python program.")
    print("Choose a game or learning exercise to run.")


GAME_MENU: List[Tuple[str, Callable[[], None]]] = [
    ("Guessing Game", run_guessing_game),
    ("Word Scramble", run_word_scramble),
    ("Math Quiz", run_math_quiz),
    ("Tic Tac Toe", run_tic_tac_toe),
    ("Adventure Game", run_adventure_game),
]


def list_game_titles() -> List[str]:
    return [title for title, _ in GAME_MENU]


def main_menu() -> None:
    while True:
        clear_screen()
        print_welcome_message()
        titles = list_game_titles() + ["Quit"]
        choice = choose_option("Choose a mini-app:", titles)
        if choice == len(titles) - 1:
            print("Goodbye!")
            break
        _, action = GAME_MENU[choice]
        action()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mega Program — 500-line Python utility suite")
    parser.add_argument(
        "--game",
        choices=[title.lower().replace(" ", "_") for title, _ in GAME_MENU],
        help="Run a single game directly.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for repeatable behavior.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    if args.game is None:
        main_menu()
        return
    normalized = args.game
    mapping: Dict[str, Callable[[], None]] = {
        title.lower().replace(" ", "_"): action for title, action in GAME_MENU
    }
    if normalized in mapping:
        mapping[normalized]()
    else:
        print(f"Unknown game: {normalized}")
        sys.exit(1)


if __name__ == "__main__":
    main()
