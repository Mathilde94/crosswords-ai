import random

from typing import List


class WordsRepository:
    def __init__(self, words):
        self.words = words

    def get_random_words(self, n: int = 3) -> List[str]:
        words = []
        for i in range(n):
            new_word = random.choice(self.words)
            while new_word in words:
                new_word = random.choice(self.words)
            words.append(random.choice(self.words))
        words.sort(key=lambda x: len(x))
        words.reverse()
        return words

    @staticmethod
    def build_from(words):
        return WordsRepository(words)


words_repository = WordsRepository.build_from("""horse
pepperoni
pizza
pie
fruit
pasta
tomato
sauce
cheese
bacon
banana
dog""".split("\n"))
