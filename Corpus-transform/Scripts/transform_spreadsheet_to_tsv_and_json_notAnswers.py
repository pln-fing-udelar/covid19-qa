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
FilesInput.append('../DatasetCovid/covid_qa_dev.csv')

FileInputDocs = '../DatasetCovid/Articles.tsv'

FileOutputCSV = '../DatasetCovid/dataset_covid_qa_dev_notAnswers.tsv'
FileOutputJson = '../DatasetCovid/dataset_covid_qa_dev_notAnswers.json'

id_autogen = 0

# section to create json
# format: SQUAD format

data = list()
Add_item = False 

with open(FileOutputCSV, 'w') as f:
    writer = csv.writer(f, delimiter="\t")

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

                    tsv_file = csv.reader(fileQuestions, delimiter=",")

                    for line in tsv_file:
                        ID  = line[0]

                        if (docID == ID):
                            # Flag to indicate there is a question for this document
                            Add_item = True
                            # Flag to indicate the question is already on the dataset
                            QuestionAlready = False

                            # Extract info from tsv of questions and answers
                            question = str(line[1])
                            anotator = line[2]
                            sentenceAnswer = str(line[3])
                            answer = sentenceAnswer.partition("[")[2].partition("]")[0] 
                            FirstSplit = sentenceAnswer.partition("[")
                            SecondSplit = FirstSplit[2].partition("]")
                            sentenceAnswer = FirstSplit[0] + SecondSplit[0] + SecondSplit[2]
                            
                            # here we don't iterate because we have just one answer for line
                            item_answer = dict()
                            item_answer["text"] = answer
                            if answer =="":
                                item_answer["answer_start"] = -1
                            else:
                                #item_answer["answer_start"] = text.find(answer)
                                startSentenceAnswer = text.find(sentenceAnswer)
                                startAnswerOnSentenceAnswer = sentenceAnswer.find(answer)
                                item_answer["answer_start"] = startSentenceAnswer + startAnswerOnSentenceAnswer

                            # There is on the dictonary the same question?
                            for it in item_paragraph['qas']:
                                if it["question"] == question:
                                    QuestionAlready = True
                                    item2 = it
                                    break

                            if not QuestionAlready: 
                                item_qas = dict()
                                item_qas["question"] = question
                                item_qas['id'] = id_autogen
                                #item_qas['answers'] = list()
                                #item_qas['answers'].append(item_answer)
                                id_autogen += 1
                                item_paragraph['qas'].append(item_qas)
                            #else:
                                #item2['answers'].append(item_answer) 

                fileQuestions.close()

            if Add_item:
                item["paragraphs"].append(item_paragraph)
                data.append(item)
                Add_item = False
                """
                # Code for tsv
                for i in item_paragraph['qas']:
                    question = i["question"]
                    writeAnswer = "["
                    for i_a in i['answers']:
                        if writeAnswer == "[":
                            writeAnswer = writeAnswer + "'" + i_a["text"] + "'"
                        else:
                            writeAnswer = writeAnswer + ", '" + i_a["text"] + "'"
                    writeAnswer = writeAnswer + "]"
                    writer.writerow([question, writeAnswer])  
                """
    fileArticles.close()

f.close()

jsondict = dict()
jsondict["data"] = data

# write dict into json file
with codecs.open(FileOutputJson, 'w', encoding="utf-8") as jsonFile:
    json.dump(jsondict, jsonFile, indent = 4, ensure_ascii=False)
    jsonFile.close()

