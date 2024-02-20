import logging
import queue

from crosswords.service.tasks.executor import Executor

log = logging.getLogger(__name__)


class ThreadPool:
    """Pool to simulate threads consuming tasks from a queue."""
    MAX_EXECUTORS = 5

    def __init__(self, nb_workers=MAX_EXECUTORS):
        self.nb_workers = nb_workers
        self.queue = queue.Queue()
        self.workers = [Executor(identifier, self.queue) for identifier in range(nb_workers)]
        self.start()

    def start(self):
        for worker in self.workers:
            worker.start()

    def process(self, crossword_id, tries):
        self.queue.put((crossword_id, tries))
        log.info(f"Background crossword task queued: {crossword_id}")


thread_pool = ThreadPool()
