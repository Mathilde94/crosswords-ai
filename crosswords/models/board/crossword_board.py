from __future__ import annotations

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
            self.words_positions[word] = ((position[0] - min_x, position[1] - min_y), direction)

    def __str__(self):
        output = "Words: {words}.\n".format(words=self.words_positions)
        return output + super().__str__()

    def __copy__(self):
        new_board = CrosswordBoard(self.width, self.height)
        new_board.matrix = [[self.matrix[i][j] for j in range(self.width)] for i in range(self.height)]
        new_board.words_positions = self.words_positions.copy()
        return new_board

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
