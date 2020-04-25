#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
import xml.etree.ElementTree as ET

PATH_ARTICLES_FOLDER = "data/la_diaria_v1"


def generate_corpus_from_json(file_name: str) -> None:
    """Given a JSON containing news, creates several files according to our XML schema """
    with open(os.path.join(PATH_ARTICLES_FOLDER, file_name)) as file:
        articles = json.load(file)["articles"]

    for i, article in enumerate(articles, start=1):
        create_xml_file(i, article["html"], article["slug"])


def create_xml_file(id_: int, html: str, slug: str) -> None:
    date = re.split(r"-", re.search(r'<time[^>]*datetime="(\d+-\d+-\d+).', html).group(1))  # get article date

    year = date[0]
    month = date[1]
    day = date[2]
    xml_id = "t" + str(id_).zfill(4)
    txt = re.sub(r"<.*?>", "", html) # clean html tags
    txt = re.sub(r'\d+ De \w+ De \d+ \|', "",txt) # clean date
    
    capture_title = re.split('\s{3,}',txt) # title is surrounded by whitespaces
    txt = re.sub(capture_title[1],'',txt,1)
    

    article = ET.Element('article') # create xml
    
    article.set("id", xml_id)
    article.set("date", year + "-" + month + "-" + day)
    article.set("title",capture_title[1])
    article.set("url", "https://ladiaria.com.uy/articulo/" + year + "/" + month + "/" + slug)
    article.set("src", "ladiaria")

    article.text = txt

    with open(os.path.join(PATH_ARTICLES_FOLDER, xml_id + ".xml"), "w") as file:
        file.write('\n'.join(ET.tostringlist(article, encoding='unicode')))


if __name__ == "__main__":
    generate_corpus_from_json("la_diaria_v1.json")
            