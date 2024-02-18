import asyncio
import unittest

from unittest import mock

from crosswords.llm.constants import LLAMA_FINETUNED_SERVER
from crosswords.llm.prompt_interface import PromptInterface


class TestPromptInterface(unittest.TestCase):
    def test_initialization(self):
        prompt_interface = PromptInterface()
        llm_interface = prompt_interface.llm_interface
        self.assertTrue(llm_interface.url, LLAMA_FINETUNED_SERVER)

    @mock.patch('crosswords.llm.interface.LLMInterface.make_call', return_value="response")
    def test_llm_execute(self, mock_make_call):
        prompt_interface = PromptInterface()
        response = prompt_interface.llm_execute(new_tokens=3, t=0.5)
        self.assertEqual(response, "response")

    def test_execute(self):
        prompt_interface = PromptInterface()
        with self.assertRaises(NotImplementedError):
            asyncio.run(prompt_interface.execute())
