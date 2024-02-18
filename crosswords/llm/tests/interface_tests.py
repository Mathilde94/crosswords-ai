import json
import unittest

from unittest import mock

from crosswords.llm.constants import LLAMA_FINETUNED_SERVER
from crosswords.llm.interface import LLMInterface


def mock_post_llm_call(*args, **kwargs):
    class MockResponse:
        data = json.loads(kwargs.get("data"))
        response_content = "response from prompt: {prompt} (tokens={tokens}, t={t})".format(
            prompt=data.get("prompt"),
            tokens=data.get("n_predict"),
            t=data.get("temperature"),
        )
        content = bytes('{{"content": "{}"}}'.format(response_content), 'utf-8')
    return MockResponse()


class TestLLMInterface(unittest.TestCase):
    def test_initialization(self):
        interface = LLMInterface()
        self.assertTrue(interface.url, LLAMA_FINETUNED_SERVER)

    @mock.patch('requests.post', mock_post_llm_call)
    def test_make_call(self):
        interface = LLMInterface()
        response_content = interface.make_call("prompt here", new_tokens=3, t=0.5)
        self.assertEqual(response_content, "response from prompt: prompt here (tokens=3, t=0.5)")
