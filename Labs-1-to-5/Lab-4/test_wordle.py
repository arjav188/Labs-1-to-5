"""Tests for feedback and game flow (stdlib unittest only).

Author: arjav.chandranath | SRN: PES2UG24CS080
Run: python -m unittest -v
"""
import unittest

from feedback import evaluate
from game import WordleGame, Session, WON, LOST, QUIT
from words import words_of_length, SUPPORTED_LENGTHS

G, Y, X = "green", "yellow", "gray"


def scripted(inputs):
    it = iter(inputs)
    out = []
    return (lambda prompt="": next(it)), out.append, out


class TestFeedback(unittest.TestCase):
    def test_original_bug_extra_copies_are_gray(self):
        # crane has ONE e (exact, last slot): extra e's gray; r is present
        self.assertEqual(evaluate("crane", "eerie"), [X, X, Y, X, G])

    def test_array_vs_grape(self):
        # grape: g r a p e -> guess a r r a y
        # r(1) exact; a(0) present; r(2) gray (only one r); a(3) gray (only one a); y gray
        self.assertEqual(evaluate("grape", "array"), [Y, G, X, X, X])

    def test_exact_all_green(self):
        self.assertEqual(evaluate("stone", "stone"), [G] * 5)

    def test_absent_all_gray(self):
        self.assertEqual(evaluate("stone", "fjklb"), [X] * 5)

    def test_present_wrong_position(self):
        self.assertEqual(evaluate("plant", "tnalp"), [Y, Y, G, Y, Y])

    def test_two_copies_in_target(self):
        # apple has two p's; guess "pppxx" style
        self.assertEqual(evaluate("apple", "ppzzz"), [Y, G, X, X, X])
        self.assertEqual(evaluate("apple", "zppzz"), [X, G, G, X, X])

    def test_exact_takes_priority_over_earlier_present(self):
        # target "eerie" guess "seeds": e(1),e(2)? target e e r i e
        # s gray, e(1) green, e(2) present? target idx2='r' so not exact; pool has e (idx0,idx4)
        self.assertEqual(evaluate("eerie", "eeeee"), [G, G, X, X, G])

    def test_lengths_4_and_6(self):
        self.assertEqual(evaluate("moon", "noon"), [X, G, G, G])
        self.assertEqual(evaluate("moon", "ooxx"), [Y, G, X, X])
        # little vs letter: l,t,t exact; first e present; second e gray (one e in target... pool has one e)
        self.assertEqual(evaluate("little", "letter"), [G, Y, G, G, X, X])
        self.assertEqual(evaluate("coffee", "effect"), [Y, Y, G, Y, Y, X])

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            evaluate("apple", "app")


class TestGame(unittest.TestCase):
    def test_invalid_guesses_do_not_consume_turns_or_history(self):
        inp, out, log = scripted(["abc", "toolong", "12345", "ab cd", "", "crane", "q"])
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), QUIT)
        self.assertEqual(len(g.history), 1)  # only "crane"
        self.assertEqual(sum("Invalid" in m for m in log), 5)

    def test_win_on_first_guess(self):
        inp, out, log = scripted(["stone"])
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), WON)
        self.assertEqual(len(g.history), 1)

    def test_win_on_final_guess(self):
        inp, out, log = scripted(["apple"] * 5 + ["stone"])
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), WON)
        self.assertEqual(len(g.history), 6)

    def test_loss_after_six_accepted_guesses(self):
        inp, out, log = scripted(["apple"] * 6)
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), LOST)
        self.assertEqual(len(g.history), 6)
        self.assertTrue(any("STONE" in m for m in log))

    def test_invalid_between_valid_still_allows_six(self):
        seq = ["apple", "x", "apple", "yy", "apple", "apple", "zzzzzz", "apple", "apple"]
        inp, out, log = scripted(seq)
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), LOST)
        self.assertEqual(len(g.history), 6)

    def test_quit_immediately(self):
        inp, out, log = scripted(["q"])
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), QUIT)
        self.assertEqual(g.history, [])

    def test_eof_acts_as_quit(self):
        def inp(_):
            raise EOFError
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=lambda *_: None)
        self.assertEqual(g.run(), QUIT)

    def test_history_printed_after_each_accepted_guess(self):
        inp, out, log = scripted(["crane", "abc", "stone"])
        g = WordleGame(5, target="stone", input_fn=inp, output_fn=out)
        g.run()
        self.assertEqual(sum(m.startswith("\nHistory") for m in log), 2)

    def test_all_lengths_have_words_and_play(self):
        for n in SUPPORTED_LENGTHS:
            self.assertTrue(words_of_length(n))
            target = words_of_length(n)[0]
            inp, out, log = scripted([target])
            self.assertEqual(WordleGame(n, input_fn=inp, output_fn=out, target=target).run(), WON)

    def test_wrong_length_for_mode_is_invalid(self):
        inp, out, log = scripted(["moons", "moon"])
        g = WordleGame(4, target="moon", input_fn=inp, output_fn=out)
        self.assertEqual(g.run(), WON)
        self.assertEqual(len(g.history), 1)

    def test_unsupported_mode_rejected(self):
        with self.assertRaises(ValueError):
            WordleGame(7)


class TestSession(unittest.TestCase):
    def test_summary_counts(self):
        import game
        orig = game.random.choice
        game.random.choice = lambda seq: seq[0]
        try:
            # 4-letter: moon (win), then 5-letter loss, then quit game
            inp, out, log = scripted(["4", "moon", "5", "crane", "crane", "crane",
                                      "crane", "crane", "crane", "6", "q", "q"])
            s = Session(input_fn=inp, output_fn=out)
            s.run()
        finally:
            game.random.choice = orig
        text = "\n".join(log)
        self.assertIn("Session summary", text)
        self.assertIn("arjav.chandranath", text)
        self.assertIn("PES2UG24CS080", text)
        self.assertIn("Games: 3  Won: 1  Lost: 1  Quit: 1", text)

    def test_bad_length_reprompts(self):
        inp, out, log = scripted(["7", "abc", "q"])
        Session(input_fn=inp, output_fn=out).run()
        self.assertEqual(sum("Please enter one of" in m for m in log), 2)
        self.assertIn("No games played.", "\n".join(log))


if __name__ == "__main__":
    unittest.main()
