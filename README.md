

Uploading video_5.mov…

# AI Powered Crosswords

## Introduction
This project is a simple implementation of a crossword puzzle solver using AI.

## Main Components

### Fine-tuning LLama13b
After running and testing llama13B locally, I tested getting crosswords clues from given words. Even after giving a few 
single shot examples in prompts, examples were mitigated. Clues were either definitions of the word itself or would 
contain the word or had very wrong formatting.  

Hence, I decided to fine tune the model on a dataset of crosswords clues and answers. I used the dataset from the New
York Times crosswords in [kaggle](https://www.kaggle.com/datasets/darinhawley/new-york-times-crossword-clues-answers-19932021).

After fine-tuning it on my AWS account, I downloaded the main necessary files for the model and ran the inference on my local M2 mac.

Comparing before and after with the fine tune models:
![llama_models_comparison.jpeg](media%2Fllama_models_comparison.jpeg)

Once I got a better model to generate clues from given words, I created a few components that help extracting concepts 
from any content, generating a small crossword puzzle. 

### Crosswords generation
A few modules in the crosswords domain:
- `models` that contain the crossword board, clues, context and concept models
- `service` that contains the main logic to generate a crossword:
  - `concepts` to extract words from any text content when we want to generate a crossword from a specific content
  - `clues` to generate clues and their explanations from a word
  - `tasks` for the background tasks that creates the crosswords
- `repository` that contains the crosswords sessions in Redis and a list of popular words available if we want to generate crosswords from random words.
- `llm` that contains the logic to integrate with a background LLM and all the prompts directory

### API server and frontend
- FastAPI server under `crosswords/<main|controllers>` that contain the main APIs routers
- Webpack to serve the UI under `frontend`

## How to

### Fine-tuning LLama13b
Please check the readme under `fine_tuning` for more details on fine tuning steps and how to run locally 
the fine-tuned inference model.

### Running backend server
To run and/or develop on the crosswords FastAPI server, please check the README.md under `crosswords`.

### Running frontend server
To run and/or develop on the crosswords UI frontend, please check the README.md under `frontend`.

Example of local crossword being generated:
(Note: local fine-tuned LLama13B server takes requests sequentially which makes a full new crossword generation taking a few seconds)

![crossword_ex_1](./media/crossword_ex_1.png)
![crossword_ex_2](./media/crossword_ex_2.png)



https://github.com/Mathilde94/crosswords-ai/assets/1518309/8c03d092-4478-4e79-8614-f78677debcf3






