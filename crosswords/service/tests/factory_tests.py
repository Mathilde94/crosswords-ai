import asyncio
import unittest

from crosswords.models.board.exceptions import TooManyWordsError
from crosswords.service.tasks.factory import CrosswordFactory


class TestFactory(unittest.TestCase):
    def test_factory_fails_initialization_with_more_than_limit_words(self):
        with self.assertRaises(TooManyWordsError):
            CrosswordFactory.from_words(
                ["word"] * (CrosswordFactory.LIMIT_CONCEPTS_WORDS + 1)
            )

    def test_factory_initialization(self):
        factory = CrosswordFactory.from_words(["word"], 15, 20)
        self.assertEqual(factory.concepts[0].word, "word")
        self.assertEqual(factory.width, 15)
        self.assertEqual(factory.height, 20)
        self.assertEqual(factory.finished_crosswords, [])
        self.assertEqual(factory.best_crossword, None)

    def test_generate_boards(self):
        factory = CrosswordFactory.from_words(["word", "another", "one"])
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(factory.finished_crosswords), 19)
        self.assertEqual(len(best_crossword.words_positions), 3)

    def test_generate_boards_and_iterate_over_missing_words(self):
        """chzsy would not be added at first, until raspberry is added first."""
        factory = CrosswordFactory.from_words(["pie", "pear", "chzsy", "raspberry"])
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(best_crossword.words_positions), 4)

    def test_generate_boards_missing_word(self):
        factory = CrosswordFactory.from_words(["word", "another", "one", "missig"])
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(best_crossword.words_positions), 3)
        self.assertFalse("missig" in best_crossword.words_positions)

    def test_can_not_touch_extremity_words(self):
        factory = CrosswordFactory.from_words(["wold", "dive", "war", "rmm"])
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(best_crossword.words_positions), 3)

    def test_generate_boards_more_words(self):
        factory = CrosswordFactory.from_words(
            [
                "inactive",
                "ethernet",
                "botany",
                "kings",
                "token",
                "kiev",
                "meek",
                "osha",
                "ari",
                "inc",
            ]
        )
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(best_crossword.words_positions), 9)

    def test_generate_boards_more_words(self):
        factory = CrosswordFactory.from_words(
            [
                x["word"]
                for x in [
                    {"word": "persist"},
                    {"word": "merlin"},
                    {"word": "please"},
                    {"word": "exert"},
                    {"word": "cesar"},
                    {"word": "nudge"},
                    {"word": "pane"},
                    {"word": "emir"},
                    {"word": "ohm"},
                    {"word": "red"},
                ]
            ]
        )
        best_crossword = asyncio.run(factory.generate_best_board())
        self.assertEqual(len(best_crossword.words_positions), 9)
        print(best_crossword)
