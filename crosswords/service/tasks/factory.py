from __future__ import annotations

import asyncio
import threading
import time
from typing import Dict, List, Tuple

from collections import deque

from crosswords.models.concept import Concept
from crosswords.models.board.crossword_board import CrosswordBoard
from crosswords.models.board.exceptions import TooManyWordsError


def get_letter_intersections(word1: str, word2: str) -> Dict[int, Tuple[int, str]]:
    """Get the intersections between two words"""
    intersections = {}
    for i, letter1 in enumerate(word1):
        for j, letter2 in enumerate(word2):
            if letter1 == letter2:
                intersections[i] = (j, letter1)
    return intersections


class CrosswordFactory:
    LIMIT_CONCEPTS_WORDS = 15
    TOP_INTERMEDIARY_CROSSWORDS = 100
    INCREMENT_NEW_WORDS = 2
    INITIAL_WORDS_BATCH = 5

    def __init__(self, concepts: List[Concept], width=50, height=50):
        if len(concepts) > self.LIMIT_CONCEPTS_WORDS:
            raise TooManyWordsError(
                "Please provide less than {} words".format(
                    CrosswordFactory.LIMIT_CONCEPTS_WORDS
                )
            )
        self.concepts = concepts
        self.words = [concept.word for concept in concepts]
        self.width = width
        self.height = height
        self.queue_crosswords = None
        self.finished_crosswords = []
        self.best_crossword = None

    async def generate_best_board(self) -> CrosswordBoard:
        start_time = int(time.time())
        self.finished_crosswords = self.build_initial_board_set(
            self.words[: CrosswordFactory.INITIAL_WORDS_BATCH]
        )
        for i in range(
            int(
                max(
                    0,
                    (len(self.words) - CrosswordFactory.INITIAL_WORDS_BATCH)
                    / CrosswordFactory.INCREMENT_NEW_WORDS,
                )
            )
            + 1
        ):
            next_words = self.words[
                : CrosswordFactory.INITIAL_WORDS_BATCH
                + (CrosswordFactory.INCREMENT_NEW_WORDS * i)
            ]
            self.build_from_boards(self.finished_crosswords, next_words)
            # clean up and take top ones so far on that iteration
            max_number_words = max(
                [len(board.words_positions) for board in self.finished_crosswords]
            )
            self.finished_crosswords = [
                c
                for c in self.finished_crosswords
                if len(c.words_positions) == max_number_words
            ]
            self.finished_crosswords = list(set(self.finished_crosswords))
            self.finished_crosswords.sort()
            self.finished_crosswords = self.finished_crosswords[
                : CrosswordFactory.TOP_INTERMEDIARY_CROSSWORDS
            ]

        for board_index in range(len(self.finished_crosswords)):
            self.finished_crosswords[board_index].trim()

        self.finished_crosswords.sort(key=lambda x: x.density, reverse=True)

        # Set the best board
        self.best_crossword = self.finished_crosswords[0]
        print(
            "Done generating the board.... Took: ",
            int(time.time()) - start_time,
            " seconds",
        )
        return self.best_crossword

    def build_initial_board_set(self, words: List[str] = None):
        initial_crosswords = []
        for word in words:
            c = CrosswordBoard(self.width, self.height)
            c.set_first_word(word)
            initial_crosswords.append(c)
        return initial_crosswords

    def build_from_boards(
        self, crosswords: List[CrosswordBoard], words: List[str] = None
    ):
        print("Building board set including: ", words)
        initial_crosswords = deque(crosswords)
        max_number_words = 1
        while initial_crosswords:
            if max_number_words < len(words):
                max_number_words = max(
                    [len(board.words_positions) for board in initial_crosswords]
                )
            current_board = initial_crosswords.pop()
            if len(current_board.words_positions) == len(words):
                self.finished_crosswords.append(current_board)
            else:
                missing_words = list(set(words) - set(current_board.words_positions))
                missing_words.sort()
                for missing_word in missing_words:
                    new_boards = CrosswordFactory.next_boards_with_word(
                        current_board, missing_word
                    )
                    if (
                        len(new_boards) == 0
                        and len(current_board.words_positions) >= max_number_words
                    ):
                        self.finished_crosswords.append(current_board)

                    for b in new_boards:
                        if b not in initial_crosswords:
                            initial_crosswords.append(b)

    @staticmethod
    def next_boards_with_word(
        initial_board: CrosswordBoard, word: str
    ) -> List[CrosswordBoard]:
        """Return all boards generated by adding the word to the current board."""
        boards = []
        # Iterate over already placed words: if the word intersects with any of them, try to place it
        words_positions = initial_board.words_positions.copy()
        for w, placement in words_positions.items():
            w_direction = placement[1]
            w_position = placement[0]
            opposite_direction = (w_direction[1], w_direction[0])
            intersections = get_letter_intersections(w, word)
            if not intersections:
                continue
            for i, (j, letter) in intersections.items():
                # we need to go the opposite direction from the word w
                new_start = (
                    w_position[0]
                    + i * opposite_direction[1]
                    - j * opposite_direction[0],
                    w_position[1]
                    + i * opposite_direction[0]
                    - j * opposite_direction[1],
                )
                new_board = initial_board.__copy__()
                word_placed = new_board.place_word(word, opposite_direction, new_start)
                if word_placed and new_board not in boards:
                    new_board.words_positions[word] = (new_start, opposite_direction)
                    boards.append(new_board)

        return boards

    @staticmethod
    def from_words(words: List[str], width=20, height=20) -> CrosswordFactory:
        concepts = [Concept(word) for word in words]
        return CrosswordFactory(concepts, width, height)
