import asyncio
import unittest

from unittest import mock

from crosswords.models.concept import Concept
from crosswords.service.clues.generator import ClueGenerator
from crosswords.llm.prompts.clues import GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE


def patch_get_clue_from_llm(*args, **kwargs):
    return "clue_for_{word}".format(word=kwargs.get('word'))


class TestClueGenerator(unittest.TestCase):
    word = "inheritance"
    title = "Python for intermediate"
    section = "Object Oriented Programming"
    concepts = [Concept(c) for c in ["inheritance", "super", "composition", "class", "attributes"]]

    def test_initialization(self):
        generator = ClueGenerator()
        self.assertTrue(generator.template, GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE)

    def test_prepare_prompt(self):
        generator = ClueGenerator()
        prompt = generator.prepare_prompt(self.word, self.title, self.section, self.concepts)
        self.assertTrue("The word to guess is: INHERITANCE" in prompt)
        self.assertTrue("title: Python for intermediate" in prompt)
        self.assertTrue("section: Object Oriented Programming" in prompt)

    @mock.patch('crosswords.llm.prompt_interface.PromptInterface.llm_execute', patch_get_clue_from_llm)
    def test_execute(self):
        generator = ClueGenerator()
        clues = asyncio.run(generator.execute(self.concepts, self.title, self.section))
        self.assertEqual([c.clue for c in clues], ["clue_for_{}".format(concept.word) for concept in self.concepts])
