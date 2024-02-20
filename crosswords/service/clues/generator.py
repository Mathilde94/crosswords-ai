from typing import List

from crosswords.llm.prompt_interface import PromptInterface

from crosswords.llm.prompts.clues import (
    CONTENT_CONTEXT,
    GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE,
)
from crosswords.models.clue import Clue
from crosswords.models.concept import Concept

from .constants import MOCKED_CLUE


class ClueGenerator(PromptInterface):
    template = GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE
    MOCKED_RESPONSE = MOCKED_CLUE

    def prepare_prompt(
        self,
        word: str,
        title: str = "",
        section: str = "",
        concepts: List[Concept] = None,
    ) -> str:
        context = ""
        if title and section and concepts:
            context = CONTENT_CONTEXT.format(
                title=title,
                section=section,
                concepts=", ".join([c.word for c in concepts]),
            )
        return self.template.format(word=word.upper(), context=context)

    async def execute(
        self,
        concepts: List[Concept],
        title: str = "",
        section: str = "",
        tries: int = 1,
    ) -> List[Clue]:
        clues = []
        for concept in concepts:
            for _ in range(tries):
                clue_text = self.llm_execute(
                    word=concept.word, title=title, section=section, concepts=concepts
                )
                if clue_text == "" or "response:" in clue_text.lower():
                    continue
                clue = Clue(concept.word, clue_text)
                clues.append(clue)
        return clues
