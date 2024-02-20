import asyncio

from crosswords.models.concepts import Concept
from crosswords.models.board.factory import CrosswordFactory
from crosswords.service.concepts.extractor import ConceptExtractor
from crosswords.service.clues.generator import ClueGenerator
from crosswords.service.clues.explanations import ClueExplanationOperator

concepts_extractor = ConceptExtractor()
clues_generator = ClueGenerator()
clues_explanation_operator = ClueExplanationOperator()


async def get_clues(concepts, title, section, tries=3):
    clues = await clues_generator.execute(concepts, title=title, section=section, tries=tries)
    explainable_clues = await clues_explanation_operator.execute(clues)
    return explainable_clues


async def main():
    title = "JavaScript from Beginner to Expert"
    section = "Conditional Statements"
    extracts = """hello today we're going to talk about conditional statements"""
    # concepts = await concepts_extractor.execute(title, section, extracts)
    concepts = ["else", "instruction", "conditional", "debug", "function"]
    print("Concepts", concepts)
    crosswords_factory = CrosswordFactory([Concept(c) for c in concepts])
    clues, best_crossword = await asyncio.gather(
        get_clues(concepts, title=title, section=section, tries=3),
        crosswords_factory.generate_boards()
    )
    print()
    for clue in clues:
        print(clue)
    print("\nBest Crossword", best_crossword)


if __name__ == "__main__":
    asyncio.run(main())
