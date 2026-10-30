"""Letter-evaluation rules for Wordle.

Author: arjav.chandranath | SRN: PES2UG24CS080
"""
from collections import Counter

GREEN = "green"    # exact: right letter, right position
YELLOW = "yellow"  # present: right letter, wrong position
GRAY = "gray"      # absent: no unmatched copy left in the target


def evaluate(target, guess):
    """Return a list of GREEN/YELLOW/GRAY, one per letter of `guess`.

    Standard Wordle rules, works for any word length:
      Pass 1 - mark exact matches (green) and remove those target letters
               from the pool of letters still available.
      Pass 2 - left to right, a non-green letter is yellow only if the pool
               still holds a copy of it (each target letter is used at most
               once); otherwise it is gray.
    """
    if len(target) != len(guess):
        raise ValueError("target and guess must have the same length")

    result = [GRAY] * len(guess)
    pool = Counter()  # target letters not consumed by an exact match

    for i, ch in enumerate(guess):
        if ch == target[i]:
            result[i] = GREEN
        else:
            pool[target[i]] += 1

    for i, ch in enumerate(guess):
        if result[i] == GREEN:
            continue
        if pool[ch] > 0:
            result[i] = YELLOW
            pool[ch] -= 1
    return result
