BAD_CLUE_EXPLANATION = "I can't find a good explanation for this clue"


class Clue:
    def __init__(self, word: str, clue: str = "", explanation: str = ""):
        self.word = word
        self.clue = clue
        self.explanation = explanation

    def set_clue(self, clue: str):
        self.clue = clue

    def set_explanation(self, explanation: str):
        self.explanation = explanation

    def is_valid(self):
        return (
            self.explanation != BAD_CLUE_EXPLANATION
            # and self.explanation != ""
            and self.clue != ""
            and "response:" not in self.clue.lower()
            and (self.word.lower() not in self.clue.lower())
            and ("across" not in self.clue.lower() and "down" not in self.clue.lower())
        )

    def __str__(self):
        return "<Word: {}, Clue: {} (Explanation: {})>".format(
            self.word, self.clue, self.explanation
        )

    def serialize(self):
        return {"word": self.word, "clue": self.clue, "explanation": self.explanation}
