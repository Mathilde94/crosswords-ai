import unittest

from crosswords.models.board.crossword_board import CrosswordBoard


class TestCrosswordBoard(unittest.TestCase):
    def test_initialization(self):
        board = CrosswordBoard()
        self.assertEqual(board.width, 20)
        self.assertEqual(board.height, 20)
        self.assertEqual(board.words_positions, {})
        self.assertEqual(board.initial_position, (10, 5))
        self.assertEqual(board.initial_direction, (0, 1))

    def test_add_first_word(self):
        board = CrosswordBoard()
        self.assertTrue(board.set_first_word("word"))
        self.assertEqual(board.words_positions, {"word": ((10, 5), (0, 1))})

    def test_trim_to_single_row_for_first_word(self):
        board = CrosswordBoard()
        self.assertTrue(board.set_first_word("word"))
        self.assertEqual(board.words_positions, {"word": ((10, 5), (0, 1))})
        board.trim()
        self.assertEqual(board.words_positions, {"word": ((0, 0), (0, 1))})
