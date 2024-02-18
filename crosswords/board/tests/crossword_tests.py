import unittest

from crosswords.board.crossword import CrosswordBoard


class TestCrossword(unittest.TestCase):
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

    def test_add_words(self):
        board = CrosswordBoard()
        self.assertTrue(board.set_first_word("word"))
        self.assertEqual(board.words_positions, {"word": ((10, 5), (0, 1))})
        new_boards = board.create_boards_with_word("another")
        self.assertEqual(len(new_boards), 2)
        self.assertEqual(new_boards[0].words_positions, {
            'word': ((10, 5), (0, 1)), 'another': ((8, 6), (1, 0))
        })
        self.assertEqual(new_boards[1].words_positions, {
            'word': ((10, 5), (0, 1)), 'another': ((4, 7), (1, 0))
        })

    def test_trim_to_single_row_for_first_word(self):
        board = CrosswordBoard()
        self.assertTrue(board.set_first_word("word"))
        self.assertEqual(board.words_positions, {"word": ((10, 5), (0, 1))})
        board.trim()
        self.assertEqual(board.words_positions, {"word": ((0, 0), (0, 1))})

    def test_trim_board_with_2_words(self):
        board = CrosswordBoard()
        self.assertTrue(board.set_first_word("word"))
        new_boards = board.create_boards_with_word("another")
        self.assertEqual(new_boards[0].words_positions, {
            'word': ((10, 5), (0, 1)), 'another': ((8, 6), (1, 0))
        })
        new_boards[0].trim()
        self.assertEqual(new_boards[0].words_positions, {
            'another': ((0, 1), (1, 0)), 'word': ((2, 0), (0, 1))
        })
