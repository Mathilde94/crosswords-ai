import enum

from typing import List

from crosswords.models.context import CrosswordContext
from crosswords.models.board.crossword_board import CrosswordBoard
from crosswords.models.clue import Clue
from crosswords.models.concept import Concept
from crosswords.repository.crosswords import crossword_repository


class Status(enum.Enum):
    CREATED = "created"
    COMPLETED = "completed"
    ERROR = "error"


class Crossword:
    def __init__(
        self,
        context: CrosswordContext,
        id: str = None,
        status: Status = Status.CREATED,
        clues: List[Clue] = None,
        board: CrosswordBoard = CrosswordBoard(),
        concepts: List[Concept] = None,
    ):
        self.id = id or None
        self.context = context
        # Attributes that would need to be set later if not provided
        self.clues: List[Clue] = clues or []
        self.board: CrosswordBoard = board
        self.concepts: List[Concept] = concepts or []
        self.status = status

    def set_concepts(self, concepts: List[Concept]):
        self.concepts = concepts

    def set_clues(self, clues: List[Clue]):
        self.clues = clues

    def get_ordered_clues(self):
        words_orders = self.board.words_positions.copy()
        words_orders = list(words_orders.items())
        words_orders.sort(
            key=lambda item: (item[1][0][0], item[1][0][1])
        )
        ordered_clues = []
        for word, _ in words_orders:
            for clue in self.clues:
                if clue.word == word:
                    ordered_clues.append(clue)
                    break
        return ordered_clues

    def set_board(self, board: CrosswordBoard):
        self.board = board

    def set_status(self, status: Status):
        self.status = status

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status.value,  # default to "created" if status is not set
            "concepts": [concept.serialize() for concept in self.concepts],
            "clues": [clue.serialize() for clue in self.get_ordered_clues()],
            "board": self.board.serialize(),
            "context": self.context.serialize(),
        }

    @staticmethod
    def from_serialized(data: dict):
        return Crossword(
            id=data["id"],
            status=Status(data["status"]),
            context=CrosswordContext.from_serialized(data["context"]),
            clues=[Clue(**clue) for clue in data["clues"]],
            board=CrosswordBoard.from_serialized(data["board"]),
            concepts=[Concept(**concept) for concept in data["concepts"]],
        )

    @staticmethod
    def get_from_db(crossword_id):
        serialized_crossword = crossword_repository.get(crossword_id)
        return Crossword.from_serialized(serialized_crossword)

    def create(self):
        self.id = crossword_repository.create()
        self.save()
        return self.id

    def save(self):
        if not self.id:
            raise Exception("Can not save a crossword without an id")
        else:
            crossword_repository.save(self.id, self.serialize())

    def delete(self):
        crossword_repository.delete(self.id)

    def verify(self, matrix: List[List[str]]):
        return self.board.verify(matrix)


class CrosswordBuilder:
    def __init__(self, context: CrosswordContext):
        self.context = context
        self.concepts: List[Concept] = []

    def add_concepts(self, concepts: List[Concept]):
        self.concepts += concepts

    def build(self):
        return Crossword(self.context, concepts=self.concepts)
