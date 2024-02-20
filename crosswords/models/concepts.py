class Concept:
    def __init__(self, word: str):
        self.word = word

    def serialize(self):
        return {
            "word": self.word
        }

    def __lt__(self, other):
        return self.word < other.word