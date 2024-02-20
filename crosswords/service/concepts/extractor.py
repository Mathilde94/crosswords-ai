from typing import List

from crosswords.llm.prompt_interface import PromptInterface
from crosswords.llm.prompts.concepts import EXTRACT_CONCEPTS
from crosswords.models.concept import Concept
from crosswords.service.concepts.extract_strategy import SimpleParagraphExtractStrategy


class ConceptExtractor(PromptInterface):
    MAX_LENGTH_CONCEPT = 20
    MIN_LENGTH_CONCEPT = 2

    template = EXTRACT_CONCEPTS
    extracts_strategy = SimpleParagraphExtractStrategy()

    async def execute(self, title: str, section: str, extracts: str) -> List[Concept]:
        words = []
        for extract in self.extracts_strategy.split(extracts):
            w = self.llm_execute(title=title, section=section, extract=extract)
            if "_title" in w or w == "":
                continue
            words += w.split(",")
        words = list(set(words))
        flat_words = []
        for w in words:
            flat_words += [
                a.strip()
                for a in w.split(" ")
                if (
                    a != ""
                    and self.MAX_LENGTH_CONCEPT > len(a) > self.MIN_LENGTH_CONCEPT
                )
            ]
        return [Concept(c) for c in list(set(flat_words))]
