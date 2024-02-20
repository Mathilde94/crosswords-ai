import logging
import queue

from crosswords.service.tasks.executor import Executor

log = logging.getLogger(__name__)
global_thread_pool = None


class ThreadPool:
    """Pool to simulate threads consuming tasks from a queue."""

    MAX_EXECUTORS = 5

    def __init__(self, nb_workers=MAX_EXECUTORS):
        self.nb_workers = nb_workers
        self.queue = queue.Queue()
        self.workers = [
            Executor(identifier, self.queue) for identifier in range(nb_workers)
        ]
        self.start()

    def start(self):
        for worker in self.workers:
            worker.start()

    def process(self, crossword_id, tries):
        self.queue.put((crossword_id, tries))
        log.info(f"Background crossword task queued: {crossword_id}")


def get_thread_pool():
    global global_thread_pool
    if global_thread_pool is None:
        global_thread_pool = ThreadPool()
    return global_thread_pool
