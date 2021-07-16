import re
import os
import html
import calendar
from urllib.request import urlopen,Request

#### GLOBAL VARIABLES ####

PATH_ARTICLES_FOLDER = "data/articles"

url1 = "https://www.montevideo.com.uy/tag/CoronavirusUy?pl=2035"
url2 = "https://www.montevideo.com.uy/clave/Coronavirus?pl=2035"
url3 = "https://www.montevideo.com.uy/tag/covid19?pl=2035"
current_id = 1

# Download the source code of the webpage
def download_url_content(url):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = Request(url, None, headers)
    response = urlopen(req)
    page = response.read()
    response.close()
    decoded = html.unescape(page.decode('utf-8'))
    return decoded

# Given the source code of the webpage, returns a list with its articles
def extract_articles(url_content):
    articles = re.findall(r'<article.*?</article>', url_content, re.DOTALL)
    return articles

# Removes duplicates from the article list, based on their urls
def remove_duplicates(articles):
    article_dict = {}
    for article in articles:
        url = re.search(r'url=\"(.*?)\"', article).group(1)
        if url: 
            article_dict[url] = article
    
    return article_dict.values()

def month_string_to_number(month_string):
    return str(list(calendar.month_abbr).index(month_string)).zfill(2)


def fix_date(article):
    date_tag_re = r'date=\".*?(\d{1,2})\s(\w{3})\s(\d{4}).*?\"'
    date_tag = re.search(date_tag_re, article) 
    article = re.sub(date_tag_re, 'date="{}-{}-{}"'.format(date_tag.group(3), month_string_to_number(date_tag.group(2)), date_tag.group(1).zfill(2)), article)
    return article


# All articles have the same id, so we need to create and set a different id for each article manually
def generate_ids(article):
    global current_id
    article_id = f"{current_id:04d}"
    current_id += 1
    return re.sub(r'id=\"t\d{1,5}"', 'id="mp{}"'.format(article_id), article)

# Removes HTML tags from an article
def clean_article(article):
    main_tag = re.search(r'<article.*?>', article, re.DOTALL) 
    article = re.sub(r'<br>', '<br>\n', article)
    while re.search(r'<[^>]*>', article):
        article = re.sub(r'<[^>]*>', '', article)
    
    article = re.sub(r']]>', '', article)
    article = re.sub(r'\t\t', '', article, re.MULTILINE)
    article = main_tag.group(0) + article + '</article>'
    return article

# Creates an XML file for each of the articles
def create_xml_files(articles):
    for article in articles:
        article_id = re.search(r'id=\"(mp\d{1,5})"', article).group(1)
        with open(os.path.join(PATH_ARTICLES_FOLDER, article_id + ".xml"), "w") as file:
            file.write(article)

def main():
    articles = extract_articles(download_url_content(url1)) + extract_articles(download_url_content(url2)) + extract_articles(download_url_content(url3))
    articles = remove_duplicates(articles)
    articles = [fix_date(article) for article in articles]
    articles = [generate_ids(article) for article in articles]
    articles = [clean_article(article) for article in articles]
    create_xml_files(articles)
