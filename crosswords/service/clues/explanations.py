from typing import List

from crosswords.llm.prompt_interface import PromptInterface
from crosswords.models.clue import Clue
from crosswords.service.clues.prompts.constants import CLUE_EXPLANATION


class ClueExplanationOperator(PromptInterface):
    template = CLUE_EXPLANATION

    async def execute(self, clues: List[Clue]) -> List[Clue]:
        for clue in clues:
            clue.set_explanation(self.llm_execute(word=clue.word, clue=clue.clue))
        return clues
