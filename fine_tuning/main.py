import os
import boto3
import sagemaker
import csv
import json

from sagemaker.s3 import S3Uploader
from sagemaker.jumpstart.estimator import JumpStartEstimator

from .constants import AWS_DEFAULT_REGION, GET_HINT_FOR_WORD_TEMPLATE, TRAINING_SET_SIZE

os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION


def get_train_data_location():
    output_bucket = sagemaker.Session(boto3.session.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_KEY"]
    )).default_bucket()
    train_data_location = f"s3://{output_bucket}/crosswords_dataset"
    return train_data_location


def upload_to_training_s3(local_file):
    S3Uploader.upload(local_file, get_train_data_location())


def create_train_jsonl():
    clues = []
    with open('dataset/nytcrosswords.csv', encoding='utf-8', errors='ignore') as csvfile:
        crosswords_clue_reader = csv.reader(csvfile, delimiter=",")
        for row in crosswords_clue_reader:
            clues.append(row)
    jsonl_data = ""
    for clue in clues[1:TRAINING_SET_SIZE]:
        jsonl_data += json.dumps({
            "instruction": "Given a word in a crossword, provide a crossword clue for it.",
            "context": "The word to guess is: " + clue[1].replace('"', "") + ".\nProvide a clue for it:",
            "response": clue[2]
        }) + "\n"
    jsonl_data = jsonl_data.strip("\n")

    # Save it locally
    with open("dataset/train.jsonl", "w") as f:
        f.write(jsonl_data)


def upload_crossword_files_to_s3():
    upload_to_training_s3("./dataset/template.json")
    upload_to_training_s3("./dataset/train.jsonl")


def fine_tune_model():
    role = 'Sagemaker_deploy_training_role'
    model_id, model_version = "meta-textgeneration-llama-2-13b", "2.*"

    jump_start_estimator = JumpStartEstimator(
        role=role,
        model_id=model_id,
        model_version=model_version,
        environment={"accept_eula": "true"},
        disable_output_compression=True,
    )

    jump_start_estimator.set_hyperparameters(instruction_tuned="True", epoch="1", max_input_length="1024")
    jump_start_estimator.fit({"training": get_train_data_location()})
    return jump_start_estimator


def predict_finetune(fine_tuned_predictor, word: str):
    payload = {
        "inputs": GET_HINT_FOR_WORD_TEMPLATE.format(word),
        "parameters": {"max_new_tokens": 20},
    }
    fine_tuned_response = fine_tuned_predictor.predict(payload, custom_attributes="accept_eula=true")
    return fine_tuned_response


if __name__ == "__main__":
    create_train_jsonl()
    upload_crossword_files_to_s3()
    estimator = fine_tune_model()
    # fine_tuned_predictor = estimator.deploy()
    # predict_finetune(fine_tuned_predictor, "conditional")
