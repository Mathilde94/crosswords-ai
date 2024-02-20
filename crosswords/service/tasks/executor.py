import asyncio
import logging
import threading
import queue

from crosswords.models.crossword import Crossword, Status
from crosswords.service.concepts.extractor import ConceptExtractor
from crosswords.service.clues.generator import ClueGenerator
from crosswords.service.clues.explanations import ClueExplanationOperator
from crosswords.service.tasks.factory import CrosswordFactory

concepts_extractor = ConceptExtractor()
clues_generator = ClueGenerator()
clues_explanation_operator = ClueExplanationOperator()

log = logging.getLogger(__name__)


class Executor(threading.Thread):
    """Simulating individual thread polling from a shared queue of tasks to process"""
    TIMEOUT_IN_SEC = 1

    def __init__(self, identifier, queue: queue.Queue = None):
        super().__init__()
        self.identifier = identifier
        self.queue = queue

    def run(self):
        while True:
            try:
                crossword_id, tries = self.queue.get(timeout=self.TIMEOUT_IN_SEC)
            except queue.Empty:
                continue
            self.process(crossword_id, tries)
            self.queue.task_done()

    def process(self, crossword_id, tries):
        log.info(f"Processing crossword_id: {crossword_id} (thread={threading.get_native_id()})")
        self._generate(crossword_id, tries)
        log.info(f"Processing crossword_id completed: {crossword_id}")

    def _generate(self, crossword_id: str, tries: int = 1):
        # Fetch crossword from db:
        crossword = Crossword.get_from_db(crossword_id)
        context = crossword.context

        # First, generate the concepts
        concepts = asyncio.run(concepts_extractor.execute(context.title, context.section, context.extracts))
        if len(concepts) == 0:
            log.warning(f"No concepts found for crossword_id: {crossword_id}")
            return
        crossword.set_concepts(concepts)

        # Then generate the clues
        crosswords_factory = CrosswordFactory(concepts)

        clues = asyncio.run(self._get_valid_clues(concepts, title=context.title, section=context.section, tries=tries))

        # Then generate the board
        best_crossword = asyncio.run(crosswords_factory.generate_best_board())

        crossword.set_clues(clues)
        crossword.set_board(best_crossword)

        # Saving updated crossword
        crossword.set_status(Status.COMPLETED)
        crossword.save()

        return crossword.serialize()

    async def _get_valid_clues(self, concepts, title, section, tries=3):
        clues = await clues_generator.execute(concepts, title=title, section=section, tries=tries)
        explainable_clues = await clues_explanation_operator.execute(clues)
        return list(filter(lambda c: c.is_valid(), explainable_clues))
