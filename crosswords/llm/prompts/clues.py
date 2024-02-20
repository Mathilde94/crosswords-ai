GET_CLUE_FOR_WORD_IN_CONTEXT_TEMPLATE = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

Instruction:
Given a word in a crossword, provide a crossword clue for it. Other instructions: 
- The clue should not refer to any other word in the crossword hence avoid clues like "See 4-Down" or "Like 7-Across".
- The clue should also not be a direct definition of the word, but rather a hint or a riddle that leads to the word.
- The clue should be related to the context provided directly or indirectly.
- The clue should not be too easy or too hard. It should be challenging but solvable.
- The clue should not contain the word itself. 

Example:
word: IRS
clue: Tax agcy.

Example: 
word: ETHICS
clue: Field of study that asks "What should I do?"

Example:
word: ACE
clue: Card in a royal flush

Example: 
word: SAYSYES
clue: "I agree"

Example: 
word: ENIGMA
clue: ___ code

Bad example: 
word: SHE
clue: "___ in the rain"

Your turn with this context:
{context}

Input:
The word to guess is: {word}
Provide a clue for it:

Response:"""

CONTENT_CONTEXT = """This word was found in a document where:
title: {title}
section: {section}
other words in the document context: {concepts}
Return a clue that is related to this overall content."""

CLUE_EXPLANATION = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

Instruction:
Given a word to guess of a crossword and its clue, given a short explanation of why this clue is the best for this word.
If you can't find a good explanation for it, return "I can't find a good explanation for this clue".

Example:
word: ace
clue: "Card in a royal flush"
explanation: An ace is a card in a royal flush

Example:
word: IRS
clue: "Tax agcy."
explanation: IRS is an abbreviation for Internal Revenue Service which is the government tax agency

Example:
word: else
clue: Otherwise
explanation: else is a synonym of otherwise

Example: 
word: enigma
clue: "___ code"
explanation: Enigma is a code and can fill the blank of the clue

Example:
word: else
clue: "Ain\'t No Mountain High Enough" singer
explanation: I can't find a good explanation for this clue

Example:
word: she
clue: "___ in the rain"
explanation: I can't find a good explanation for this clue

Your turn:
word: {word}
clue: {clue}
explanation:"""