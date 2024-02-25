from __future__ import annotations
from typing import List

from .base import Board


HORIZONTAL_DIRECTION = (0, 1)
VERTICAL_DIRECTION = (1, 0)


class CrosswordBoard(Board):
    def __init__(self, width=20, height=20):
        super().__init__(width, height)
        self.initial_position = (int(height * 0.5), int(width * 0.25))
        self.initial_direction = HORIZONTAL_DIRECTION
        self.words_positions = {}

    def set_first_word(self, word: str) -> bool:
        result = super().place_word(word, self.initial_direction, self.initial_position)
        if result:
            self.words_positions[word] = (self.initial_position, self.initial_direction)
        return result

    def trim(self):
        min_x, max_x, min_y, max_y = self.get_borders()
        super().trim_to(min_x, max_x, min_y, max_y)
        for word, (position, direction) in self.words_positions.items():
            self.words_positions[word] = (
                (position[0] - min_x, position[1] - min_y),
                direction,
            )

    def __str__(self):
        output = "Words: {words}.\n".format(words=self.words_positions)
        return output + super().__str__()

    def __copy__(self):
        new_board = CrosswordBoard(self.width, self.height)
        new_board.matrix = [
            [self.matrix[i][j] for j in range(self.width)] for i in range(self.height)
        ]
        new_board.words_positions = self.words_positions.copy()
        return new_board

    def __hash__(self):
        ordered_words = sorted(self.words_positions.items())
        hash_string = ""
        for word in ordered_words:
            hash_string += word[0] + ":"
            hash_string += str(word[1])
            hash_string += ";"
        return hash(hash_string)

    def __lt__(self, other):
        if len(self.words_positions) == len(other.words_positions):
            # less prioritized board if the board is not balanced, meaning that the difference
            # between the width and the height is bigger
            return abs(self.width - self.height) >= abs(other.width - other.height)
        return len(self.words_positions) < len(other.words_positions)

    def serialize(self):
        data = super().serialize()
        data["words_position"] = self.words_positions
        return data

    @staticmethod
    def from_serialized(data: dict) -> CrosswordBoard:
        board = CrosswordBoard(data["width"], data["height"])
        board.matrix = data["matrix"]
        board.words_positions = data["words_position"]
        return board

    def verify(self, matrix: List[List[str]]) -> bool:
        return self.matrix == matrix
