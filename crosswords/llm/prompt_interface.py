import os

from crosswords.llm.interface import LLMInterface


class PromptInterface:
    template = ""
    MOCKED_RESPONSE = ""

    def __init__(self):
        self.llm_interface = LLMInterface()
        self.mock_data = int(os.environ.get("MOCK_DATA", 0))

    def prepare_prompt(self, *args, **kwargs):
        return self.template.format(*args, **kwargs)

    def llm_execute(self, new_tokens=20, t=0.7, *args, **kwargs) -> str:
        if self.mock_data:
            return self.MOCKED_RESPONSE.format(**kwargs)
        return self.llm_interface.make_call(
            self.prepare_prompt(*args, **kwargs), new_tokens, t
        )

    async def execute(self, *args, **kwargs):
        raise NotImplementedError
