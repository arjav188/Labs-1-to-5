# Scenario 17 — Wordle

**Author:** arjav.chandranath | **SRN:** PES2UG24CS080

A terminal Wordle-style game with duplicate-letter scoring and guess history.

## Provided files

- `main.py` — entry point.
- `game.py` — game loop and history.
- `feedback.py` — letter-evaluation rules.
- `words.py` — in-memory word list.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

## What was changed (Lab 4)

- **Task 1** `feedback.py`: two-pass evaluation with a `Counter` pool, so exact matches are
  resolved first and each target letter satisfies at most one guess letter. Original defect:
  `crane` vs `eerie` marked both extra `e`s yellow (target has one `e`).
- **Task 2** `game.py`: loop runs until six *accepted* guesses; invalid input (wrong length,
  non-letters, empty) reprints an error and does not consume a turn; clean win/loss/quit messages.
- **Task 3** `words.py`: added 4- and 6-letter words to the in-memory list; choose 4/5/6 at start.
- **Task 4** `game.py`: history printed after every accepted guess; `Session` prints a final summary.
- `test_wordle.py`: 22 stdlib `unittest` cases. Run with `python -m unittest -v`.

## Before changing the code

Read the feedback implementation carefully. Test guesses containing repeated letters
against targets that contain fewer copies of that letter than the guess.

## Task 1 — Correct duplicate-letter feedback

Implement standard Wordle-style feedback in which exact matches are resolved first and
each occurrence in the target can satisfy at most one occurrence in the guess.

**Done when:** repeated-letter guesses produce correct exact/present/absent results.

## Task 2 — Complete guess handling

Add clean win/loss handling, enforce the six accepted-guess limit, and ensure invalid
guesses do not consume a turn.

## Task 3 — Variable word lengths

Add 4-, 5-, and 6-letter modes using the supplied in-memory words. The feedback logic
must work for all supported lengths.

## Task 4 — Guess history and summary

Display a readable history after each accepted guess and provide a final session summary.
Do not duplicate entries for invalid attempts.

## Required testing

Use repeated-letter cases, exact matches, absent letters, invalid lengths, all three
word lengths, winning on the final allowed guess, losing, and quitting.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [ ] Task 1 completed and the original defect was reproduced and fixed.
- [ ] Tasks 2–4 completed and tested.
- [ ] Boundary and invalid-input cases tested.
- [ ] No unnecessary external dependencies added.
- [ ] No persistent storage added.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-05-wordle/
├── README.md
├── requirements.txt
├── main.py
├── game.py
├── feedback.py
└── words.py
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
