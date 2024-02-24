# FastAPI Server

## Setup
Note: You can also run all the backend API server and frontend with mocked data if you set up the following 
environment variable in the `.env` file:
```shell
MOCK_DATA=1
```
This can help if you dont have the LLM set up locally and want to test the rest.

```shell
# If using pyenv: 
pyenv install 3.11.5
pyenv global 3.11.5

# Create virtualenv
python -m venv ~/.virtualenvs/crosswords_ai
source ~/.virtualenvs/crosswords_ai/bin/activate
pip install -r requirements.txt
```

## Running the components

Run docker-compose to run Redis:
```shell
docker-compose up -d
```

To run the fast API server:
```shell
uvicorn crosswords.main:app --reload
```

## Testing
To test all is running, go to: http://0.0.0.0:8000/docs#/default and test `POST` and `GET` endpoints.

![crossword_post.png](../images/crosswords_post.png)
![crossword_get.png](../images/crossword_get.png)

Running file `test_clues` for an individual crossword should return something like this:
```python 
Concepts ['else', 'instruction', 'conditional', 'debug', 'function']

<Word: else, Clue: "If not, then ..." (Explanation: else is a synonym of otherwise)>
<Word: else, Clue: "In case" (Explanation: else is a synonym of in case)>
<Word: instruction, Clue: "Tell me what to do!" (Explanation: An instruction is an instruction to guess for a clue)>
<Word: instruction, Clue: What a recipe is (Explanation: Instruction is a clue for it)>
<Word: conditional, Clue: Like a "if" statement in programming (Explanation: The word to guess is "if")>
<Word: conditional, Clue: ___ statement (Explanation: Conditional is a type of statement)>
<Word: debug, Clue: Test out, as a program (Explanation: Debug is a synonym of test out)>
<Word: debug, Clue: Find and fix a bug (Explanation: Debug is a verb which means to find and fix a bug)>
<Word: debug, Clue: Test a program (Explanation: Debug is to test a program, as in "debug a new app")>
<Word: function, Clue: Word with code (Explanation: function is a clue for it)>

Best Crossword Words: {'else': ((2, 4), (0, 1)), 'instruction': ((0, 6), (1, 0)), 'conditional': ((0, 0), (0, 1)), 'debug': ((1, 4), (1, 0)), 'function': ((7, 2), (0, 1))}.
Density: 0.2892561983471074
c o n d i t i o n a l 
. . . . d . n . . . . 
. . . . e l s e . . . 
. . . . b . t . . . . 
. . . . u . r . . . . 
. . . . g . u . . . . 
. . . . . . c . . . . 
. . f u n c t i o n . 
. . . . . . i . . . . 
. . . . . . o . . . . 
. . . . . . n . . . . 
```

## Developing

- To run python tests: `python -m unittest crosswords/**/*.py`
- Running coverage:
    - `coverage run -m unittest crosswords/**/*.py`
    - `coverage report -m`
- Formatting: `python -m black crosswords`

