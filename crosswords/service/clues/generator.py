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
            clue = self._get_clue(concept.word, title, section, concepts, left_tries=tries)
            clues.append(clue)
        return clues

    def _get_clue(self, word: str, title: str, section: str, concepts: List[Concept], left_tries=0) -> Clue:
        clue_text = self.llm_execute(
            word=word, title=title, section=section, concepts=concepts
        )
        clue = Clue(word, clue_text)
        if not clue.is_valid() and left_tries > 0:
            print("Retrying again as the clue was not valid and we can try again")
            # Trying again for better LLM result luck
            return self._get_clue(word, title, section, concepts, left_tries - 1)
        return clue
