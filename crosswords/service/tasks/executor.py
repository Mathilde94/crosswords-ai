import asyncio
import logging
import threading
import queue

from crosswords.models.crossword import Crossword, Status
from crosswords.service.concepts.extractor import ConceptExtractor
from crosswords.service.tasks.helpers import get_clues_and_crossword

concepts_extractor = ConceptExtractor()

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
            except KeyboardInterrupt:
                print("Stopping thread:", self.identifier)
                return

            self.process(crossword_id, tries)
            self.queue.task_done()

    def process(self, crossword_id, tries):
        log.info(
            f"Processing crossword_id: {crossword_id} (thread={threading.get_native_id()})"
        )
        self._generate(crossword_id, tries)
        log.info(f"Processing crossword_id completed: {crossword_id}")

    def _generate(self, crossword_id: str, tries: int = 1):
        # Fetch crossword from db:
        crossword = Crossword.get_from_db(crossword_id)
        context = crossword.context

        # First, generate the concepts
        if len(crossword.concepts) == 0:
            concepts = asyncio.run(
                concepts_extractor.execute(
                    context.title, context.section, context.extracts
                )
            )
            if len(concepts) == 0:
                log.warning(f"No concepts found for crossword_id: {crossword_id}")
                return
            crossword.set_concepts(concepts)

        # Then generate the clues
        clues, best_crossword = get_clues_and_crossword(
            crossword.concepts,
            title=context.title,
            section=context.section,
            tries=tries,
        )
        crossword.set_clues(clues)
        crossword.set_board(best_crossword)
        crossword.set_status(Status.COMPLETED)
        crossword.save()

        return crossword.serialize()
