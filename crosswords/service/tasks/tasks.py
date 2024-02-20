import logging
import threading

from crosswords.service.tasks.pool import get_thread_pool

log = logging.getLogger(__name__)


async def generate_crossword_task(crossword_id: str, tries: int = 3):
    log.info(
        f"Background crossword task: {crossword_id} (thread={threading.get_native_id()})"
    )
    get_thread_pool().process(crossword_id, tries)
