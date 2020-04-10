#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import xml.etree.ElementTree as ET

from covid19_qa.dataset import PATH_ANNOTATED_FILE

logger = logging.getLogger(__name__)


def main() -> None:
    xml_tree = ET.parse(PATH_ANNOTATED_FILE)

    for snippet_element in xml_tree.getroot():
        assert snippet_element.tag == "snippet"

        snippet_id = snippet_element.attrib["id"]

        text_element = next(child_element for child_element in snippet_element if child_element.tag == "text")
        text = text_element.text

        for child_element in snippet_element:
            if child_element.tag == "question":
                question = child_element.attrib["q"]
                if question and "a_start" not in child_element.attrib:
                    answer = child_element.attrib["a"]
                    if answer:
                        q_id = child_element.attrib["id"]
                        id_ = f"{snippet_id}.{q_id}"

                        matches = re.finditer(answer, text)

                        try:
                            first_match = next(matches)
                        except StopIteration:
                            logger.error(f"For the ID {id_}, can't find the answer '{answer}' within the text.")
                            continue

                        answer_start = first_match.span()[0]

                        try:
                            next(matches)
                        except StopIteration:
                            pass
                        else:
                            logger.error(f"For the ID {id_}, the answer '{answer}' "
                                         f"occurs more than once within the text.")
                            continue
                    else:
                        answer_start = "-1"

                    child_element.set("a_start", str(answer_start))

    xml_tree.write(PATH_ANNOTATED_FILE)


if __name__ == "__main__":
    main()
