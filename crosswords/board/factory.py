from __future__ import annotations

from typing import List

from .crossword import CrosswordBoard
from .exceptions import TooManyWordsError


class CrosswordFactory:
    TOP_CROSSWORDS = 3
    LIMIT_WORDS = 10

    def __init__(self, words: List[str], width=20, height=20):
        if len(words) > self.LIMIT_WORDS:
            raise TooManyWordsError("Please provide less than 10 words")
        self.words = words
        self.width = width
        self.height = height
        self.crosswords = []
        self.best_crosswords = []
        self.best_crossword = None

    async def generate_boards(self):
        initial_crossword = CrosswordBoard(self.width, self.height)
        initial_crossword.set_first_word(self.words[0])
        self.crosswords.append(initial_crossword)
        for i in range(1, len(self.words)):
            nb_boards = len(self.crosswords)
            for index in range(nb_boards):
                self.crosswords += self.crosswords[index].create_boards_with_word(self.words[i])

        for board in self.crosswords:
            board.trim()

        # now fetch the top 5 boards:
        self.best_crosswords = sorted(
            self.crosswords,
            key=lambda x: (len(x.words_positions), x.density),
            reverse=True
        )[:self.TOP_CROSSWORDS]

        # Set the best board
        self.best_crossword = self.best_crosswords[0]
        return self.best_crossword

