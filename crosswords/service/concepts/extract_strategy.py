from typing import List


class BaseExtractStrategy:
    def split(self, text: str) -> List[str]:
        raise NotImplementedError("This method must be implemented in a subclass")


class SimpleParagraphExtractStrategy:
    MAX_LENGTH_WORD_EXTRACT = 500

    def split(self, text: str) -> List[str]:
        words = text.split(" ")
        return [
            " ".join(words[i : i + self.MAX_LENGTH_WORD_EXTRACT])
            for i in range(0, len(words), self.MAX_LENGTH_WORD_EXTRACT)
        ]
