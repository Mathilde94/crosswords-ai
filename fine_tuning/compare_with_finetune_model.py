import csv
import pandas as pd
import requests
import json

from .constants import (
    GET_HINT_FOR_WORD_TEMPLATE,
    LLAMA_FINETUNED_SERVER,
    LLAMA_NONFINETUNED_SERVER
)


def get_llm_reponse(prompt, new_tokens=20, t=0.7, finetuned=True):
    r = requests.post(
        LLAMA_FINETUNED_SERVER if finetuned else LLAMA_NONFINETUNED_SERVER,
        data=json.dumps({"temperature": t, "n_predict": new_tokens, "stream": False, "prompt": prompt}),
        headers={"Content-Type": "application/json"}
    )
    response = json.loads(r.content).get("content").strip("\n")
    return response


def get_clue_for_word(word, new_tokens=20, t=0.7, finetuned=True):
    result = get_llm_reponse(GET_HINT_FOR_WORD_TEMPLATE.format(word=word), new_tokens, t, finetuned).strip()
    if result is None:  # Try again
        result = get_llm_reponse(GET_HINT_FOR_WORD_TEMPLATE.format(word=word), new_tokens, t, finetuned).strip()
    return result


def get_clues():
    clues = []
    with open('dataset/nytcrosswords.csv', encoding='utf-8', errors='ignore') as csvfile:
        crosswords_clue_reader = csv.reader(csvfile, delimiter=",")
        for row in crosswords_clue_reader:
            clues.append(row)
    return clues


def compare():
    results = {}
    clues = get_clues()
    interesting_clues_indexes = (17, 28, 43, 50, 57, 58, 106, 107, 129, 148, 187, 237, 542021, 971, 32067, 376, 395, 396, 662, 683, 694)
    for index in interesting_clues_indexes:
        results[clues[index][1]] = {"training_data": clues[index][2]}

    # fine tuned: ./server -m models/13B-invent-clue/ggml-model-Q4_K_M.gguf -c 2048
    for word, result_word in results.items():
        results[word]["finetuned_clue"] = get_clue_for_word(word, finetuned=True)

    # on non finetuned: (launch server with non finetuned model locally)
    for word, result_word in results.items():
        results[word]["nonfinetuned_clue"] = get_clue_for_word(word, finetuned=False)

    words = [word for word, _ in results.items()]
    training_data = [a["training_data"] for _, a in results.items()]
    fine_tuned_clue = [a.get("finetuned_clue") for _, a in results.items()]
    non_fine_tuned_clue = [a.get("nonfinetuned_clue") for _, a in results.items()]
    d = {
        'word': words,
        "nyt_dataset": training_data,
        "regular_llama13b": non_fine_tuned_clue,
        "my_finetuned_llama13b": fine_tuned_clue
    }
    print(pd.DataFrame(data=d))


if __name__ == "__main__":
    compare()