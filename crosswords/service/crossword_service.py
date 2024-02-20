from typing import List

from crosswords.models.concept import Concept
from crosswords.models.context import CrosswordContext
from crosswords.models.crossword import Crossword, CrosswordBuilder


class CrosswordService:

    @staticmethod
    def create_crossword(context: CrosswordContext, concepts: List[str]) -> Crossword:
        crossword_builder = CrosswordBuilder(context)
        crossword_builder.add_concepts([Concept(c) for c in concepts])
        crossword = crossword_builder.build()
        crossword.create()
        return crossword

    @staticmethod
    def get_crossword(crossword_id: str) -> Crossword:
        serialized_crossword = Crossword.get_from_db(crossword_id)
        return serialized_crossword
