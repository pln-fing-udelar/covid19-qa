import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Iterator

from nltk import sent_tokenize

from covid19_qa.pipeline import Instance
from covid19_qa.util import chunks

PATH_DATA_FOLDER = "data/articles"
PATH_ANNOTATED_FILE = "data/annotated.xml"


@dataclass
class Document:
    id: str
    text: str


def load_documents(doc_ids: Iterator[str], path_data_folder: str = PATH_DATA_FOLDER,
                   snippet_size: int = 5) -> Iterator[Document]:
    for doc_id in doc_ids:
        file_path = os.path.join(path_data_folder, doc_id + ".xml")

        article_element = ET.parse(file_path).getroot()
        assert article_element.tag == "article"

        text = article_element.text
        sentences = sent_tokenize(text)

        for i, snippet_sentences in enumerate(chunks(sentences, snippet_size)):
            yield Document(id=f"{doc_id}.{i:02d}", text=" ".join(snippet_sentences))


def all_doc_ids(path_data_folder: str = PATH_DATA_FOLDER) -> Iterator[str]:
    for file_name in os.listdir(path_data_folder):
        if file_name.endswith(".xml"):
            yield file_name[:-4]


def load_all_annotated_instances(file_path: str = PATH_ANNOTATED_FILE) -> Iterator[Instance]:
    root = ET.parse(file_path).getroot()
    for snippet_element in root:
        assert snippet_element.tag == "snippet"

        snippet_id = snippet_element.attrib["id"]

        text_element = next(child_element for child_element in snippet_element if child_element.tag == "text")
        text = text_element.text

        for child_element in snippet_element:
            if child_element.tag == "question":
                q_id = child_element.attrib["id"]
                question = child_element.attrib["q"]
                if question:
                    answer = child_element.attrib["a"]

                    # In the file, if it's not present it means the answer couldn't be found within the text.
                    # If it's "-1", it's because the answer is empty.
                    # This ends up assigning `None` for both cases.
                    # It isn't a problem in testing time for non-empty answers,
                    # because "start" and "end" aren't gonna be used.
                    # However, note it's problematic for training.
                    answer_start = child_element.attrib.get("a_start", "-1")
                    answer_start = None if answer_start == "-1" else int(answer_start)

                    if answer:
                        answers = [{"text": answer, "answer_start": answer_start}]
                    else:
                        answers = []

                    yield Instance(qas_id=f"{snippet_id}.{q_id}", question_text=question, context_text=text,
                                   answer_text=answer, start_position_character=answer_start, is_impossible=not answer,
                                   answers=answers, title=question)
