from typing import List

from crosswords.llm.prompt_interface import PromptInterface
from crosswords.service.concepts.prompts.constants import EXTRACT_CONCEPTS
from crosswords.models.concepts import Concept


class ConceptExtractor(PromptInterface):
    MAX_LENGTH_CONCEPT = 20
    MIN_LENGTH_CONCEPT = 2
    template = EXTRACT_CONCEPTS

    async def execute(self, title: str, section: str, extracts: str) -> List[Concept]:
        words = []
        for extract in extracts.split("\n"):
            w = self.llm_execute(title=title, section=section, extract=extract)
            if "_title" in w or w == '':
                continue
            words += w.split(",")
        words = list(set(words))
        flat_words = []
        for w in words:
            flat_words += [
                a.strip() for a in w.split(" ")
                if (a != "" and self.MAX_LENGTH_CONCEPT > len(a) > self.MIN_LENGTH_CONCEPT)
            ]
        return [Concept(c) for c in list(set(flat_words))]

