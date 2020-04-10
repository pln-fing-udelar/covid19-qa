import os
import json
import re
import xml.etree.ElementTree as ET

PATH_ARTICLES_FOLDER = "data/la_diaria_v1"

def generate_corpus_from_json(json_name: str):
    """Given a JSON containing news, creates several files acording to our XML schema """

    id_counter = 1

    with open(os.path.join(PATH_ARTICLES_FOLDER, json_name)) as f:
        articles = json.load(f)["articles"]

    for article in articles:
    	create_xml_file(id_counter,article["html"],article["slug"])
    	id_counter+=1	
    
    f.close()
    pass

def create_xml_file(id: int, html: str, slug: str):

	date = re.split("-",(re.findall("datetime=\"([^>]*)T[^>]*>.*?>",html)[0])) # get article date

	year = date[0]
	month = date[1]
	day = date[2]
	xml_id = "t" + str(id).zfill(4)

	article = ET.Element('article')
	article.set("id", xml_id)
	article.set("date", year + "-" + month + "-" + day)
	article.set("url","https://ladiaria.com.uy/articulo/" +  year + "/" + month + "/" + slug)
	article.set("src","ladiaria")
	article.text = re.sub('<.*?>','',html) #clean html tags

	with open(os.path.join(PATH_ARTICLES_FOLDER, xml_id + ".xml"), "w") as f:
		f.write(ET.tostring(article, encoding='unicode'))

	f.close()
    
	pass

if __name__ == "__main__":
	generate_corpus_from_json("la_diaria_v1.json")