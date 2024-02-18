from crosswords.llm.interface import LLMInterface


class PromptInterface:
    template = ""

    def __init__(self):
        self.llm_interface = LLMInterface()

    def prepare_prompt(self, *args, **kwargs):
        return self.template.format(*args, **kwargs)

    def llm_execute(self, new_tokens=20, t=0.7, *args, **kwargs):
        return self.llm_interface.make_call(self.prepare_prompt(*args, **kwargs), new_tokens, t)

    async def execute(self, *args, **kwargs):
        raise NotImplementedError
