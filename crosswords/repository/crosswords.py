import json
import redis
import uuid

from crosswords.repository.constants import REDIS_HOST, REDIS_PORT


class CrosswordRepository:
    database_index = 0
    namespace: str = "cw:"

    def __init__(self):
        self.store = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=self.database_index
        )

    def create(self) -> str:
        return str(uuid.uuid4()).replace("-", "")

    def build_key(self, crossword_id: str) -> str:
        return f"{self.namespace}{crossword_id}"

    def save(self, crossword_id: str, serialized_crossword: dict):
        print("Saving: ", serialized_crossword)
        self.store.set(
            self.build_key(crossword_id), value=json.dumps(serialized_crossword)
        )

    def get(self, crossword_id: str):
        return json.loads(self.store.get(self.build_key(crossword_id)))

    def delete(self, crossword_id: str):
        self.store.delete(self.build_key(crossword_id))


crossword_repository = CrosswordRepository()
