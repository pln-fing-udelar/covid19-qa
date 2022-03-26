#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
import xml.etree.ElementTree as ET

PATH_JSON_FOLDER = "data/la_diaria"
PATH_ARTICLES_FOLDER = "data/articles"

def generate_corpus_from_json(file_name: str) -> None:
    """Given a JSON containing news, creates several files according to our XML schema """
    with open(os.path.join(PATH_JSON_FOLDER, file_name), encoding='utf-8') as file:
        articles = json.load(file)["articles"]

    for i, article in enumerate(articles, start=1):
        create_xml_file(i, article["html"], article["slug"])


def create_xml_file(id_: int, html: str, slug: str) -> None:
    date = re.split(r"-", re.search(r'<time[^>]*datetime="(\d+-\d+-\d+).', html).group(1))  # get article date

    year = date[0]
    month = date[1]
    day = date[2]
    xml_id = "ld" + str(id_).zfill(4)
    
    title = re.search(r"<title>(.*?)</title>",  html, flags=re.DOTALL)
    article_start = re.search(r"^<.*?article-body\s*paywalled-content.*?>", html, flags=re.DOTALL)
    
    txt = html[article_start.span()[1]:]
    txt = re.sub(r"<.*?>", "", txt)  # clean html tags
    txt = re.sub(r'\d+ De \w+ De \d+ \|', "", txt)  # clean date
    txt = txt.strip()
    txt = title.group(1) + "\n" + txt
    
    article = ET.Element('article')  # create xml

    article.set("id", xml_id)
    article.set("date", year + "-" + month + "-" + day)
    article.set("title", title.group(1))
    article.set("url", "https://ladiaria.com.uy/articulo/" + year + "/" + month + "/" + slug)
    article.set("src", "ladiaria")

    article.text = txt

    with open(os.path.join(PATH_ARTICLES_FOLDER, xml_id + ".xml"), "w", encoding='utf-8') as file:
        file.write('\n'.join(ET.tostringlist(article, encoding='unicode')))


def main():
    generate_corpus_from_json("la_diaria.json")
