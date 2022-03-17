import nltk
import pandas as pd
import csv

FileInputDocs = 'DatasetCovid/Articles.tsv'

def remove_special_chars(text,char_list):
    for char in char_list:
        text=text.replace(char,'')
    return text.replace(u'\xa0', u' ')   


def process_Articles_csv():
    chars = ['\n']
    
    df = pd.DataFrame(columns=['id', 'sentence', 'title'])

    with open(FileInputDocs) as file:
        articles = csv.reader(file, delimiter="\t")
    
        for line in articles:
            
            docID = line[0]
            article = line[1]
            title = line[2]    
            
            sentences = nltk.sent_tokenize(article)
            
            lens = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
            texts = []
            current_Sentence = sentences[0]
            current_len = lens[0]
            
            
            for i in range(1, len(sentences)):
                lenSentencia = lens[i]
                Sentencia = sentences[i]
                # si me pasé del largo con el nuevo, me quedo con lo que tenia antes y seteo currents
                if lenSentencia + current_len > 450:
                    texts.append(current_Sentence)
                    current_Sentence = sentences[i]
                    current_len = lens[i]
                # sino agrego la sentencia a la current sentence y le seteo largo para proxima iteracion for
                else:
                    current_Sentence = current_Sentence + " " + Sentencia
                    current_len = current_len + 1 +  lenSentencia

            texts.append(current_Sentence)
 
            temp_df = pd.DataFrame(
                {'id': [docID]*len(texts),
                'sentence': texts,
                'title': [title]*len(texts),
                })
            df = df.append(temp_df)
        
        return df

df = process_Articles_csv()
df.to_csv('DatasetCovid/ArticlesSplit.tsv' , sep = '\t', index=False)
