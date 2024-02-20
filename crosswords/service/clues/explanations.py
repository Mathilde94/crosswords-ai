from typing import List

from crosswords.llm.prompt_interface import PromptInterface
from crosswords.llm.prompts.clues import CLUE_EXPLANATION
from crosswords.models.clue import Clue

from .constants import MOCKED_EXPLANATION


class ClueExplanationOperator(PromptInterface):
    template = CLUE_EXPLANATION
    MOCKED_RESPONSE = MOCKED_EXPLANATION

    async def execute(self, clues: List[Clue]) -> List[Clue]:
        for clue in clues:
            clue.set_explanation(self.llm_execute(word=clue.word, clue=clue.clue))
        return clues
