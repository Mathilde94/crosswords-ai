from __future__ import annotations
from typing import List, Tuple


HORIZONTAL_DIRECTION = (0, 1)
VERTICAL_DIRECTION = (1, 0)


class Board:
    EMPTY_CELL = ". "

    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.matrix = self.initialize_matrix()

    def initialize_matrix(self) -> List[List[str]]:
        return [
            [self.EMPTY_CELL for _ in range(self.width)] for _ in range(self.height)
        ]

    def place_word(
        self, word: str, direction: Tuple[int, int], start: Tuple[int, int]
    ) -> bool:
        """Place a word on the board"""
        if not self._can_place_word(word, direction, start):
            return False
        x, y = start
        dx, dy = direction
        for letter in word:
            self.matrix[x][y] = "{} ".format(letter)
            x += dx
            y += dy
        return True

    def _can_place_word(
        self, word: str, direction: Tuple[int, int], start: Tuple[int, int]
    ) -> bool:
        """Check if a word can be placed on the board"""
        x, y = start
        dx, dy = direction
        # Is the letter BEFORE the start of the word empty?
        if (
            self._is_valid_position(x - dx, y - dy)
            and self.matrix[x - dx][y - dy] != self.EMPTY_CELL
        ):
            return False

        for letter in word:
            if not self._is_valid_position(x, y):
                return False
            # We can place a word if either the cell is empty or the cell is already filled with the same letter
            if (
                self.matrix[x][y] != self.EMPTY_CELL
                and self.matrix[x][y].strip() != letter
            ):
                return False
            if self.matrix[x][
                y
            ].strip() != letter and not self._does_not_have_neighbors(x, y, direction):
                return False
            x += dx
            y += dy

        # Is the letter AFTER the end of the word empty?
        if self._is_valid_position(x, y) and self.matrix[x][y] != self.EMPTY_CELL:
            return False
        return True

    def _is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def _does_not_have_neighbors(
        self, x: int, y: int, direction: Tuple[int, int]
    ) -> bool:
        """Check if a cell does not have any neighbors"""
        if direction == HORIZONTAL_DIRECTION:
            # we want to place the word horizontally so we need to check the cells above and below
            if x == 0:
                return self.matrix[x + 1][y] == self.EMPTY_CELL
            if x == self.height - 1:
                return self.matrix[x - 1][y] == self.EMPTY_CELL
            return self.matrix[x - 1][y] == self.matrix[x + 1][y] == self.EMPTY_CELL
        # we want to place the word vertically so we need to check the cells to the left and right
        if y == 0:
            return self.matrix[x][y + 1] == self.EMPTY_CELL
        if y == self.width - 1:
            return self.matrix[x][y - 1] == self.EMPTY_CELL
        return self.matrix[x][y - 1] == self.matrix[x][y + 1] == self.EMPTY_CELL

    def get_borders(self) -> List[int]:
        # Find the lowest and highest x and y coordinates
        min_x, max_x, min_y, max_y = self.height, 0, self.width, 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != self.EMPTY_CELL:
                    min_x = min(min_x, i)
                    max_x = max(max_x, i)
                    min_y = min(min_y, j)
                    max_y = max(max_y, j)
        return [min_x, max_x, min_y, max_y]

    def trim_to(self, min_x: int, max_x: int, min_y: int, max_y: int):
        self.width = max_y - min_y + 1
        self.height = max_x - min_x + 1
        new_matrix = self.initialize_matrix()
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                new_matrix[i - min_x][j - min_y] = self.matrix[i][j]
        self.matrix = new_matrix

    @property
    def density(self) -> float:
        """Calculate the density of the board"""
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] != self.EMPTY_CELL:
                    count += 1
        return count / (self.height * self.width)

    def __str__(self):
        output = ""
        for i in range(self.height):
            for j in range(self.width):
                output += self.matrix[i][j]
            output += "\n"
        return output

    def serialize(self):
        return {"matrix": self.matrix, "width": self.width, "height": self.height}
