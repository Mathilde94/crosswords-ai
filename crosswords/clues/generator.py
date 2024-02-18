from typing import List

from crosswords.llm.prompt_interface import PromptInterface

from crosswords.clues.models import Clue
from crosswords.clues.prompts.constants import CONTENT_CONTEXT, GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE


class ClueGenerator(PromptInterface):
    template = GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE

    def prepare_prompt(self, word, title: str = '', section: str = '', concepts: List = None) -> str:
        context = CONTENT_CONTEXT.format(title=title, section=section, concepts=", ".join(concepts))
        return self.template.format(word=word.upper(), context=context)

    async def execute(self, concepts, title: str = '', section: str = '', tries: int = 1) -> List[Clue]:
        clues = []
        for concept in concepts:
            for _ in range(tries):
                clue = self.llm_execute(word=concept, title=title, section=section, concepts=concepts)
                clues.append(Clue(concept, clue))
        return clues
