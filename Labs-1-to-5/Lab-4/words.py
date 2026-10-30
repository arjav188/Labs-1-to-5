"""In-memory word list (no files or databases). Supports 4-, 5- and 6-letter modes.

Author: arjav.chandranath | SRN: PES2UG24CS080
"""
SUPPORTED_LENGTHS = (4, 5, 6)

WORDS = [
    # 4 letters
    "moon", "tree", "door", "lamp", "fish", "noon", "cool", "game",
    # 5 letters (original list)
    "apple", "array", "eerie", "crane", "grape",
    "stare", "steam", "stone", "plant", "flame",
    # 6 letters
    "little", "bottle", "garden", "summer", "planet", "coffee", "pepper", "letter",
]


def words_of_length(length):
    """Return all words of exactly `length` letters."""
    return [w for w in WORDS if len(w) == length]
