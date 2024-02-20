import asyncio
import unittest

from crosswords.models.board.exceptions import TooManyWordsError
from crosswords.models.board.factory import CrosswordFactory


class TestFactory(unittest.TestCase):
    def test_factory_fails_initialization_with_more_than_limit_words(self):
        with self.assertRaises(TooManyWordsError):
            CrosswordFactory.from_words(["word"] * 11)

    def test_factory_initialization(self):
        factory = CrosswordFactory.from_words(["word"], 15, 20)
        self.assertEqual(factory.concepts[0].word, "word")
        self.assertEqual(factory.width, 15)
        self.assertEqual(factory.height, 20)
        self.assertEqual(factory.crosswords, [])
        self.assertEqual(factory.best_crosswords, [])
        self.assertEqual(factory.best_crossword, None)

    def test_generate_boards(self):
        factory = CrosswordFactory.from_words(["word", "another", "one"])
        best_crossword = asyncio.run(factory.generate_boards())
        self.assertEqual(len(factory.crosswords), 8)
        self.assertEqual(len(factory.best_crosswords), 3)
        self.assertEqual(len(best_crossword.words_positions), 3)
        self.assertEqual(best_crossword.words_positions["word"], ((6, 0), (0, 1)))
        self.assertEqual(best_crossword.words_positions["another"], ((0, 2), (1, 0)))
        self.assertEqual(best_crossword.words_positions["one"], ((1, 1), (0, 1)))

    def test_generate_boards_missing_word(self):
        factory = CrosswordFactory.from_words(["word", "another", "one", "missig"])
        best_crossword = asyncio.run(factory.generate_boards())
        self.assertEqual(len(factory.crosswords), 8)
        self.assertEqual(len(best_crossword.words_positions), 3)
