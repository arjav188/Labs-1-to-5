"""Game loop, guess history and session summary.

Author: arjav.chandranath | SRN: PES2UG24CS080
"""
import random
import sys

from feedback import evaluate, GREEN, YELLOW
from words import SUPPORTED_LENGTHS, words_of_length

MAX_GUESSES = 6
AUTHOR = "arjav.chandranath"
SRN = "PES2UG24CS080"

WON, LOST, QUIT = "won", "lost", "quit"

_ANSI = {GREEN: "\033[30;42m", YELLOW: "\033[30;43m", "gray": "\033[97;100m"}
_PLAIN = {GREEN: "*", YELLOW: "?", "gray": "-"}


def render(guess, feedback, color=None):
    """Format one guess. Coloured tiles on a terminal, plain marks otherwise
    (* exact, ? present, - absent)."""
    if color is None:
        color = sys.stdout.isatty()
    if color:
        return " ".join(f"{_ANSI[f]} {c.upper()} \033[0m" for c, f in zip(guess, feedback))
    return " ".join(f"{c.upper()}{_PLAIN[f]}" for c, f in zip(guess, feedback))


def banner():
    return f"Wordle by {AUTHOR} ({SRN})"


class WordleGame:
    def __init__(self, length=5, target=None, input_fn=input, output_fn=print, show_banner=True):
        if length not in SUPPORTED_LENGTHS:
            raise ValueError(f"length must be one of {SUPPORTED_LENGTHS}")
        self.length = length
        self.target = target or random.choice(words_of_length(length))
        self.history = []          # accepted guesses only: (guess, feedback)
        self.outcome = None        # WON / LOST / QUIT once finished
        self._input = input_fn
        self._print = output_fn
        self._show_banner = show_banner

    def _print_history(self):
        self._print("\nHistory:")
        for n, (guess, fb) in enumerate(self.history, 1):
            self._print(f"  {n}/{MAX_GUESSES}  {render(guess, fb)}")
        self._print("")

    def _read_guess(self):
        """Prompt until a valid guess (or 'q'). Invalid input never counts."""
        while True:
            try:
                guess = self._input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return "q"
            if guess == "q":
                return "q"
            if len(guess) != self.length:
                self._print(f"Invalid: word must be exactly {self.length} letters.")
            elif not (guess.isascii() and guess.isalpha()):
                self._print("Invalid: use letters a-z only.")
            else:
                return guess

    def run(self):
        if self._show_banner:
            self._print(banner())
        self._print(f"{self.length}-letter mode, {MAX_GUESSES} guesses. "
                    "(* exact, ? wrong spot, - absent; 'q' to quit)")
        while len(self.history) < MAX_GUESSES:
            guess = self._read_guess()
            if guess == "q":
                self.outcome = QUIT
                self._print(f"Quit. The word was: {self.target.upper()}")
                return self.outcome
            self.history.append((guess, evaluate(self.target, guess)))
            self._print_history()
            if guess == self.target:
                self.outcome = WON
                self._print(f"Solved in {len(self.history)}/{MAX_GUESSES}!")
                return self.outcome
        self.outcome = LOST
        self._print(f"Out of guesses. The word was: {self.target.upper()}")
        return self.outcome


class Session:
    """Runs several games and prints a final summary. State is in memory only."""

    def __init__(self, input_fn=input, output_fn=print):
        self._input = input_fn
        self._print = output_fn
        self.games = []  # finished WordleGame objects

    def _ask_length(self):
        options = "/".join(map(str, SUPPORTED_LENGTHS))
        while True:
            try:
                raw = self._input(f"Word length ({options}), or 'q' to finish: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return None
            if raw == "q":
                return None
            if raw.isdigit() and int(raw) in SUPPORTED_LENGTHS:
                return int(raw)
            self._print(f"Please enter one of: {options}.")

    def run(self):
        self._print(banner())
        while True:
            length = self._ask_length()
            if length is None:
                break
            game = WordleGame(length, input_fn=self._input, output_fn=self._print,
                              show_banner=False)
            game.run()
            self.games.append(game)
            if game.outcome == QUIT:
                break
        self.summary()

    def summary(self):
        p = self._print
        p("\n===== Session summary =====")
        p(f"Player: {AUTHOR} ({SRN})")
        won = sum(g.outcome == WON for g in self.games)
        lost = sum(g.outcome == LOST for g in self.games)
        quit_ = sum(g.outcome == QUIT for g in self.games)
        p(f"Games: {len(self.games)}  Won: {won}  Lost: {lost}  Quit: {quit_}")
        for n, g in enumerate(self.games, 1):
            p(f"  Game {n}: {g.length} letters, word {g.target.upper()}, "
              f"{g.outcome.upper()}, {len(g.history)} guess(es)")
            for guess, fb in g.history:
                p(f"      {render(guess, fb)}")
        if not self.games:
            p("  No games played.")
