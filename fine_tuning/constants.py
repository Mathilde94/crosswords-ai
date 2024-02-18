GET_HINT_FOR_WORD_TEMPLATE = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

Instruction:
Given a word in a crossword, provide a crossword clue for it.

Input:
The word to guess is: {word}
Provide a clue for it:

Response:"""

# Ran locally on GPU
LLAMA_FINETUNED_SERVER = "http://localhost:8080/completion"
LLAMA_NONFINETUNED_SERVER = "http://localhost:8080/completion"

TRAINING_SET_SIZE = 30000

AWS_DEFAULT_REGION = "us-west-2"
