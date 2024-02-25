import asyncio
import concurrent

from typing import List


from crosswords.models.concept import Concept
from crosswords.service.tasks.factory import CrosswordFactory
from crosswords.service.clues.generator import ClueGenerator


clues_generator = ClueGenerator()


def generate_clues(concepts, title, section, tries):
    return asyncio.run(
        clues_generator.execute(concepts, title=title, section=section, tries=tries)
    )


def generate_board(factory):
    return asyncio.run(factory.generate_best_board())


def get_clues_and_crossword(
    concepts: List[Concept], title: str, section: str, tries: int = 1
):
    crosswords_factory = CrosswordFactory(concepts)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_clues = executor.submit(generate_clues, concepts, title, section, tries)
        future_best_crossword = executor.submit(generate_board, crosswords_factory)
        clues = future_clues.result()
        best_crossword = future_best_crossword.result()

    return clues, best_crossword


if __name__ == "__main__":
    concepts = [Concept(word="apple"), Concept(word="banana"), Concept(word="orange")]
    get_clues_and_crossword(concepts, "Fruits", "Fruits Section", 1)
