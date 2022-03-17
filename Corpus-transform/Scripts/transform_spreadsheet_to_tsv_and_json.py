#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: luciabouza
"""
import json
import codecs
import csv

# Variables of input and output data
FilesInput = list()
FilesInput.append('DatasetCovid/Anotación Tarea 1  y Tarea 2 - Preguntas Tarea 1.tsv')
FilesInput.append('DatasetCovid/Anotación Tarea 1  y Tarea 2 - Preguntas Tarea 2.tsv')

FileInputDocs = 'DatasetCovid/Articles.tsv'
FileOutputCSV = 'DatasetCovid/DatasetCovid.tsv'
FileOutputJson = 'DatasetCovid/DatasetCovid.json'

id_autogen = 0

# section to create csv
# format: pregunta	[‘respuesta 1’, ‘respuesta 2’, ‘respuesta 3’]
with open(FileOutputCSV, 'w') as f:
    writer = csv.writer(f, delimiter="\t")

    for i in range(len(FilesInput)):

        with open(FilesInput[i]) as file:

            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                question = str(line[1])
                sentenceAnswer = str(line[3])
                answer = sentenceAnswer.partition("[")[2].partition("]")[0]  #va a haber una sola respuesta?
                writeAnswer = "["+"'"+answer+"'"+"]" #no todas tienen el formato correcto
                writer.writerow([question, writeAnswer])      
        file.close() 

    f.close()

# section to create json
# format: SQUAD format

data = list()
Add_item = False 

with open(FileInputDocs) as fileArticles:

    Articles = csv.reader(fileArticles, delimiter="\t")

    for line in Articles:
        # Extract info from tsv of Articles
        docID = line[0]
        text = line[1]
        title = line[2]

        item = dict()
        item["title"] = title
        item["paragraphs"] = list()

        # Paragraph will contain all text of the news, therefore we don't iterate
        item_paragraph = dict()
        item_paragraph['context'] = text
        item_paragraph['qas'] = list()
        
        # Set flag to false
        Add_item = False
        
        for i in range(len(FilesInput)):

            with open(FilesInput[i]) as fileQuestions:

                tsv_file = csv.reader(fileQuestions, delimiter="\t")

                for line in tsv_file:
                    ID  = line[0]

                    if (docID == ID):
                        # Flag to indicate there is a question for this document
                        Add_item = True
                        # Extract info from tsv of questions and answers
                        question = str(line[1])
                        anotator = line[2]
                        sentenceAnswer = str(line[3])
                        answer = sentenceAnswer.partition("[")[2].partition("]")[0] 
                         
                        item_qas = dict()
                        item_qas["question"] = question
                        item_qas['id'] = id_autogen
                        item_qas['answers'] = list()
                        
                        # here we don't iterate because we have just one answer
                        item_answer = dict()
                        item_answer["text"] = answer
                        item_answer["answer_start"] = 0 # no yet implemented
                        item_qas['answers'].append(item_answer)

                        item_paragraph['qas'].append(item_qas)

                        id_autogen += 1

            fileQuestions.close()

        if Add_item:
            item["paragraphs"].append(item_paragraph)
            data.append(item)
            Add_item = False

fileArticles.close()

jsondict = dict()
jsondict["data"] = data

# write dict into json file
with codecs.open(FileOutputJson, 'w', encoding="utf-8") as jsonFile:
    json.dump(jsondict, jsonFile, indent = 4, ensure_ascii=False)
    jsonFile.close()

