import json
import redis
import uuid

from .constants import REDIS_HOST, REDIS_PORT


class CrosswordRepository:
    database_index = 0

    def __init__(self):
        self.store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=self.database_index)

    def create(self) -> str:
        return str(uuid.uuid4()).replace("-", "")

    def save(self, crossword_id: str, serialized_crossword: dict):
        print("Saving: ", serialized_crossword)
        self.store.set(
            crossword_id,
            value=json.dumps(serialized_crossword)
        )

    def get(self, crossword_id: str):
        return json.loads(self.store.get(crossword_id))

    def delete(self, crossword_id: str):
        self.store.delete(crossword_id)


crossword_repository = CrosswordRepository()
