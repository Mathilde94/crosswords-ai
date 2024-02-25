import asyncio

from typing import List

from crosswords.models.concept import Concept
from crosswords.repository.words import get_words_repository
from crosswords.service.tasks.factory import CrosswordFactory
from crosswords.service.concepts.extractor import ConceptExtractor
from crosswords.service.clues.generator import ClueGenerator
from crosswords.service.clues.explanations import ClueExplanationOperator

words_repository = get_words_repository()
concepts_extractor = ConceptExtractor()
clues_generator = ClueGenerator()
clues_explanation_operator = ClueExplanationOperator()


async def get_clues(concepts: List[Concept], title: str, section: str, tries=3):
    return await clues_generator.execute(
        concepts, title=title, section=section, tries=tries
    )
    # explainable_clues = await clues_explanation_operator.execute(clues)
    # return explainable_clues


async def get_clues():
    title = "JavaScript from Beginner to Expert"
    section = "Conditional Statements"
    extracts = """Main concepts we will be learning: statement, conditional, if/else, debug, block"""
    concepts = await concepts_extractor.execute(title, section, extracts)
    concepts = [Concept(w) for w in words_repository.get_random_words(7)]
    words = ["pie", "pear", "cheesy", "raspberry"]
    concepts = [Concept(w) for w in words]
    print("Concepts", [c.word for c in concepts])
    crosswords_factory = CrosswordFactory(concepts)
    clues, best_crossword = await asyncio.gather(
        get_clues(concepts, title=title, section=section, tries=0),
        crosswords_factory.generate_best_board(),
    )
    print()
    for clue in clues:
        print(clue)
    print("\nBest Crossword", best_crossword)


if __name__ == "__main__":
    asyncio.run(get_clues())
