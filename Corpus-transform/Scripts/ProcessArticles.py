import glob
import re
import csv
import pandas as pd

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    match = re.search(r'<.*? id="(.*?)" .*? title="(.*?)" .*?>', text)
    docID = match.group(1)
    title = match.group(2)
    return docID, title, re.sub(clean, '', text)

def remove_special_chars(text,char_list):
    for char in char_list:
        text=text.replace(char,' ')
    return text.replace(u'\xa0', u' ')   

def process_article_files(article_files):
    chars = ['\n', '\t']
    df = pd.DataFrame(columns=['id', 'article', 'title'])

    for article_file in article_files:
        with open(article_file, encoding='utf-8') as f:
            content = f.read()
        
        content = remove_special_chars(content,chars) 
        docID, title, text = remove_html_tags(content) 
        
        temp_df = pd.DataFrame(
            {'id': [docID],
             'article': [text],
             'title': [title],
            })
        df = df.append(temp_df)
    
    return df



articles_files = []

for filename in glob.iglob('../DatasetCovid/corpus/*'):
    articles_files.append(filename)
    
df = process_article_files(articles_files)
df.to_csv('../DatasetCovid/Articles.tsv' , sep = '\t', index=False)
