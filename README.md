# AI Question Generator: Question Generation Script based on T5 Pretrained Model

English | [中文](README-cn.md)

Welcome to the T5 Fine-tuned Questionnaire Generation System project! This project provides a set of tools and scripts for generating questionnaires using the T5 large pre-trained language model. With this system, you can easily generate high-quality questionnaires for various purposes, such as surveys, assessments, and data collection.

## Background

The T5 model is a state-of-the-art language model that has been pre-trained on a large corpus of text data. By fine-tuning this model on specific tasks, such as questionnaire generation, we can leverage its language understanding capabilities to generate relevant and coherent questions.

This project aims to simplify the process of fine-tuning the T5 model for questionnaire generation and provide a user-friendly interface for generating questionnaires.

## Project Structure
1. [Training.ipynb](./Training.ipynb): Training script
2. [Validation.ipynb](./Validation.ipynb): Performance testing script
3. [Data provider](./data_provider/): Toolkit (Training data preparation)

    + Data Preparation
        + [docs](./data_provider/docs/): Directory for training data
        + [question_answer_pair-example.csv](./data_provider/question_answer_pair-example.csv): Preprocessed data (example)
    + Preprocessing Tools
        + [data_loader.py](./data_provider/data_loader.py): Detailed context extractor for training
        + [context_loader.py](./data_provider/context_loader.py): Implementation script for the context extractor, used in conjunction with [data_loader.py](./data_provider/data_loader.py)
        + [keyword_extractor.py](./data_provider/keyword_extractor.py): Article keyword extractor used for actual generation

## Technical Details
1. Fine-tuned T5 Model: A fine-tuned T5 pretrained model that generates syntactically correct and context-relevant questions based on input keywords and context.
    
    + Input (string): "answer: \<keyword\> \<sep\> context: \<context\>"
    + Output (string): Generated question based on the keyword and context
2. [context_loader.py](./data_provider/context_loader.py): Context extractor that searches for relevant paragraphs in the corpus based on the questions used as references in the training dataset, narrowing down the inference range and improving training efficiency. The implementation is inspired by the following tools and algorithms:

    + ElasticSearch
    + BM25
    + TF-IDF
3. [keyword_extractor.py](./data_provider/keyword_extractor.py): Keyword extractor used for actual generation. It extracts keywords from external articles for inference. The implementation is inspired by the following algorithms:

    + Text-Rank Algorithm: A keyword extraction algorithm that borrows from the Google PageRank algorithm. It uses graph structures to select summarizing keywords from long texts.
    + PageRank

## License

This project is licensed under the [MIT License](LICENSE). Please refer to the license file for more information.

---

We hope that this project helps you generate high-quality questionnaires effortlessly using the power of the T5 language model. If you have any questions or need further assistance, please don't hesitate to reach out.
