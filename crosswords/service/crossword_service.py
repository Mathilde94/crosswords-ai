import threading

from crosswords.models.context import CrosswordContext
from crosswords.models.crossword import Crossword


class CrosswordService:

    @staticmethod
    def create_crossword(context: CrosswordContext) -> Crossword:
        crossword = Crossword.from_context(context)
        crossword.create()
        return crossword

    @staticmethod
    def get_crossword(crossword_id: str) -> Crossword:
        serialized_crossword = Crossword.get_from_db(crossword_id)
        return serialized_crossword
