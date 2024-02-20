# Fine-Tuning LLama13b for crosswords

## Fine-tuning with AWS Sagemaker
This directory contains the code to fine-tune the LLama13b model for crosswords.
- Create an AWS role `Sagemaker_deploy_training_role`
- Make sure you have quota to run `ml.g5.24xlarge` instances, needed for fine-tuning llama 13b
- Go to the `fine_tuning` directory
- Run `python main.py`, monitor the progress. It should take about 1h to fine-tune the model

## Inference model
To run the inference model, you need to follow these steps:
- clone `https://github.com/ggerganov/llama.cpp` and go to `llama.cpp` directory
- download the fine-tuned model files in S3: they should be in a S3 bucket that looks like that:
    - `sagemaker-us-west-2-<id> / meta-textgeneration-llama-2-13b-<date-format>/output/model`
      ![s3_model_generated_files.png](../images%2Fs3_model_generated_files.png)
    - place them in the `models/13B-invent-clue` directory
    - the main files needed: `*.safetensors`, `tokenizer.model`, `tokenizer_config.json`, `special_tokens_map.json`, `config.json`, `generation_config.json`
- Follow the steps to convert this model in llama.cpp:
    - `python3 convert.py models/13B-invent-clue`
    - `./quantize ./models/13B-invent-clue/ggml-model-f16.gguf ./models/13B-invent-clue/ggml-model-Q4_K_M.gguf Q4_K_M`
    - `./quantize ./models/13B-invent-clue/ggml-model-Q4_K_M.gguf ./models/13B-invent-clue/ggml-model-Q4_K_M-v2.gguf COPY`

Then you can run the inference that way:
```shell
./server -m models/13B-invent-clue/ggml-model-Q4_K_M.gguf -c 2048
```
