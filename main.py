#!/usr/bin/env python
from transformers import pipeline
from xml.dom import minidom
from nltk.tokenize import sent_tokenize
import os

DATASET_PATH = './data'

def get_most_relevant_docs(dataset, question, n):
    # Given a question and a dataset, returns the 'n' most relevant docs to find the answer
    relevant_docs = ['t001','t002','t004','t005','t006','t007','t008']  # el texto t003 da error
    
    return relevant_docs # list containing 'n' text_id's

def generate_context_snippets(dataset, relevant_docs, snippet_size):
    # A snippet is a set of snippet_size sentences.
    context_snippets = []

    for text_id in relevant_docs:
        xml = minidom.parse(os.path.join(DATASET_PATH, text_id + ".xml"))
        article = xml.getElementsByTagName('article')
        article_text = article[0].firstChild.nodeValue
        sentences = sent_tokenize(article_text)
        offset = len(sentences)//snippet_size
        remainder = len(sentences) % snippet_size

        for x in range(offset):
            snippet_text = ' '.join(
                map(str, sentences[x*snippet_size:(x+1)*snippet_size]))
            context_snippets.append(snippet_text)

        if remainder > 0:
            snippet_text = ' '.join(
                map(str, sentences[offset*snippet_size:offset*snippet_size + remainder]))
            context_snippets.append(snippet_text)

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


    number_of_docs = 7 # no se está usando este valor
    snippet_size = 5
    answers = []
    docs = get_most_relevant_docs(dataset,question,number_of_docs)
    context_snippets = generate_context_snippets(dataset,docs,snippet_size)
    for context in context_snippets:
        answers.append(highlight_answer(context,question,qa_pipeline))
    
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
