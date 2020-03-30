#!/usr/bin/env python
from transformers import pipeline
from xml.dom import minidom
from nltk.tokenize import sent_tokenize
import os

DATASET_PATH = './data'

def generate_context_snippets(dataset, docs, snippet_size):
    # A snippet is a set of snippet_size sentences.
    context_snippets = []

    for text_id in docs:
        xml = minidom.parse(os.path.join(dataset, text_id + ".xml"))
        article = xml.getElementsByTagName('article')
        article_text = article[0].firstChild.nodeValue
        sentences = sent_tokenize(article_text)
        offset = len(sentences)//snippet_size
        remainder = len(sentences) % snippet_size

        for x in range(offset):
            snippet_text = ' '.join(
                map(str, sentences[x*snippet_size:(x+1)*snippet_size]))
            context_snippets.append((snippet_text,text_id))

        if remainder > 0:
            snippet_text = ' '.join(
                map(str, sentences[offset*snippet_size:offset*snippet_size + remainder]))
            context_snippets.append((snippet_text,text_id))

    return context_snippets

def highlight_answer(context,question,qa_pipeline):
    # Given a context and a question, returns a pair (highlighted answer, score)
    
    result = qa_pipeline({"question": question, "context": context}, version_2_with_negative=True)

    return result['answer'], result['score'] 

def rank_answers(answers):
    # Each element in 'answers' has a score. Returns a list sorted in descending order.
    answers.sort(reverse=True, key=lambda x: x[1])

    return answers

def qa(dataset, question):
    # Given a dataset with multiple texts, returns the top 10 most confident paragraphs with the highlighted answer.
    # Highlighted text *like this*.

    PATH_MODEL_FOLDER = './model'
    
    kwargs = {
        "model": PATH_MODEL_FOLDER,
        "config": PATH_MODEL_FOLDER,
        "tokenizer": PATH_MODEL_FOLDER,
    }

    qa_pipeline = pipeline("question-answering", **kwargs)

    snippet_size = 5
    answers = []
    docs = []

    for dirpath, dir_list, file_list in os.walk(dataset):
        for file_name in file_list:
            if file_name[-4:]==".xml":
                docs.append(file_name[:-4])

    context_snippets = generate_context_snippets(dataset,docs,snippet_size)
    for context in context_snippets:
        answers.append(highlight_answer(context[0],question,qa_pipeline))
    
    print(rank_answers(answers))

    pass

def test():
    PATH_MODEL_FOLDER = './model'
    
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
    qa(DATASET_PATH, "¿Qué criticó Da Silveira?")
