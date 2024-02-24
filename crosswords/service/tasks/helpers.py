import asyncio

from typing import List


from crosswords.models.concept import Concept
from crosswords.service.tasks.factory import CrosswordFactory
from crosswords.service.clues.generator import ClueGenerator


clues_generator = ClueGenerator()


async def get_clues_and_crossword(concepts: List[Concept], title: str, section: str, tries: int = 1):
    crosswords_factory = CrosswordFactory(concepts)
    clues, best_crossword = await asyncio.gather(
        clues_generator.execute(
            concepts, title=title, section=section, tries=tries
        ),
        crosswords_factory.generate_best_board()
    )
    return clues, best_crossword
