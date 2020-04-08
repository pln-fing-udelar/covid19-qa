from dataclasses import dataclass


@dataclass
class Snippet:
    doc_id: str
    text: str


@dataclass
class Answer:
    snippet: Snippet
    text: str
    in_context: str
    score: float
