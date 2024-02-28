from __future__ import annotations
from typing import List
from wordfreq import zipf_frequency
import os
import random

from crosswords.repository.constants import EXAMPLE_WORDS

words_repository = None


class WordsRepository:
    LOG_BIN_FREQUENCIES = {_: [] for _ in range(10)}

    def __init__(self, words: List[str]):
        print("Creating words repository from ", len(words), "words")
        self.words = [w.lower().strip("\n") for w in words]

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
    def build_from(words: List[str]) -> WordsRepository:
        return WordsRepository(words)

    @staticmethod
    def build_from_file(file_path: str) -> WordsRepository:
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                words = f.readlines()
            words = [w.lower().strip("\n") for w in words]
            words_with_frequency = [
                (w, zipf_frequency(w, "en", wordlist="small")) for w in words
            ]
            log_bin_frequencies = WordsRepository.LOG_BIN_FREQUENCIES.copy()
            for word, freq in words_with_frequency:
                log_bin_frequencies[int(freq)].append(word)
            words = (
                log_bin_frequencies[3] + log_bin_frequencies[4] + log_bin_frequencies[5]
            )
        return WordsRepository(words)


def get_words_repository():
    global words_repository
    if words_repository is None:
        path_crosswords_ai = os.path.dirname(os.path.realpath(__name__)).strip(
            "/crosswords"
        )
        file_path = "/{root}/fine_tuning/dataset/unique_words.txt".format(
            root=path_crosswords_ai
        )
        words_repository = WordsRepository.build_from_file(file_path)
    return words_repository
