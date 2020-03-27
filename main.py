#!/usr/bin/env python
from transformers import pipeline


def main():
    kwargs = {
        "model": PATH_MODEL_FOLDER,
        "config": PATH_MODEL_FOLDER,
        "tokenizer": PATH_MODEL_FOLDER,
    }

    qa_pipeline = pipeline("question-answering", **kwargs)
    
    context = "Manuel Romero está colaborando activamente con huggingface/transformers para traer el poder de las últimas técnicas de procesamiento de lenguaje natural al idioma español."
    question = "¿Para qué lenguaje está trabajando?"

    result = qa_pipeline({"question": question, "context": context}, version_2_with_negative=True)
    print(result)

if __name__ == "__main__":
    main()
