import asyncio
import unittest

from unittest import mock

from crosswords.service.concepts.extractor import ConceptExtractor
from crosswords.llm.prompts.concepts import EXTRACT_CONCEPTS


CONCEPTS_TESTS = ["attributes", "class", "composition", "object"]


def patch_get_concepts_from_llm(*args, **kwargs):
    return ", ".join(CONCEPTS_TESTS)


class TestConceptExtractor(unittest.TestCase):
    word = "inheritance"
    title = "Python for intermediate"
    section = "Object Oriented Programming"
    extracts = "This content is about composition, class, attributes, objects."

    def test_initialization(self):
        generator = ConceptExtractor()
        self.assertTrue(generator.template, EXTRACT_CONCEPTS)

    def test_prepare_prompt(self):
        generator = ConceptExtractor()
        prompt = generator.prepare_prompt(title=self.title, section=self.section, extract=self.extracts)
        self.assertTrue("title: {}".format(self.title) in prompt)
        self.assertTrue("section: {}".format(self.section) in prompt)
        self.assertTrue("extract: {}".format(self.extracts) in prompt)

    @mock.patch('crosswords.llm.prompt_interface.PromptInterface.llm_execute', patch_get_concepts_from_llm)
    def test_execute(self):
        generator = ConceptExtractor()
        concepts = asyncio.run(generator.execute(self.title, self.section, self.extracts))
        concepts.sort()
        self.assertEqual([c.word for c in concepts], CONCEPTS_TESTS)
