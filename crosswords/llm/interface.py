import requests
import json

from crosswords.llm.constants import LLAMA_FINETUNED_SERVER


class LLMInterface:
    def __init__(self):
        self.url = LLAMA_FINETUNED_SERVER

    def make_call(self, prompt: str, new_tokens: int = 20, t: float = 0.7):
        r = requests.post(
            self.url,
            data=json.dumps({"temperature": t, "n_predict": new_tokens, "stream": False, "prompt": prompt}),
            headers={"Content-Type": "application/json"}
        )
        return json.loads(r.content).get("content").strip("\n").split("\n")[0].strip()
