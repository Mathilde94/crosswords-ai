import asyncio
import unittest

from unittest import mock

from crosswords.service.clues.explanations import ClueExplanationOperator
from crosswords.models.clues import Clue
from crosswords.service.clues.prompts.constants import CLUE_EXPLANATION


def patch_get_explanation_from_llm(*args, **kwargs):
    return "explanation_for_{word}".format(word=kwargs.get('word'))


class TestClueExplanationOperator(unittest.TestCase):
    word = "inheritance"
    clue = "Clue for inheritance word"

    def test_initialization(self):
        generator = ClueExplanationOperator()
        self.assertTrue(generator.template, CLUE_EXPLANATION)

    def test_prepare_prompt(self):
        generator = ClueExplanationOperator()
        prompt = generator.prepare_prompt(word=self.word, clue=self.clue)
        self.assertTrue("word: inheritance" in prompt)
        self.assertTrue("clue: Clue for inheritance word" in prompt)
        self.assertTrue("explanation:" in prompt)

    @mock.patch('crosswords.llm.prompt_interface.PromptInterface.llm_execute', patch_get_explanation_from_llm)
    def test_execute(self):
        generator = ClueExplanationOperator()
        clues = [Clue(self.word, self.clue)]
        clues_with_explanations = asyncio.run(generator.execute([Clue(self.word, self.clue)]))
        self.assertEqual(
            [c.explanation for c in clues_with_explanations],
            ["explanation_for_{}".format(clue.word) for clue in clues]
        )
