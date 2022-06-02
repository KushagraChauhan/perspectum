'''
    This file contains the helper functions which I made along the way
'''
from flask import jsonify
import json
dataset = 'scores.json'

with open(dataset, 'r', encoding='utf-8') as data_file:    
    inputData = json.load(data_file)

'''
    Sort the submissions based on score
'''
def sort_submissions_of_items(json_list):
    for item in json_list:
        subs = item.get("submissions", [])
        if isinstance(subs, list):
            subs.sort(key=lambda x: x.get("score", 0), reverse=True)

sort_submissions_of_items(inputData)

'''
    Get names of all users
'''
def getNames():
    names = []
    for i in inputData:
        names.append(i['name'])
    return jsonify(names)

'''
    Calculate the total score of a user and output in following format:
    HashTable format = {name: submissionScore}
'''
def getScores():
    totalScore = {}
    for i in inputData:
        score = 0
        for j in i['submissions']:
            score += j['score']
        #logger.info(score)
        totalScore[i['name']] = totalScore.get(i['name'], 0) + score
    
    return jsonify(totalScore)

'''
    Check for more than 3 submissions
'''
def validUsers():
    totalScore = {}
    for i in inputData:
        score = 0
        if len(i['submissions']) >= 3:
            for j in i['submissions']:
                score += j['score']
            totalScore[i['name']] = totalScore.get(i['name'], 0) + score
    return jsonify(totalScore)

'''
    Top 24 submissions only 
    Ranking from top to bottom
'''
def bestScore():
    totalScore = {}
    for i in inputData:
        score = 0
        if len(i['submissions']) >= 3 and len(i['submissions']) <=24:
            for j in i['submissions']:
                score += j['score']
            totalScore[i['name']] = totalScore.get(i['name'], 0) + score
        
        if len(i['submissions']) > 24:
            for j in range(len(i['submissions'])):
                score += i['submissions'][j]['score']
                if j > 22:
                    break
            totalScore[i['name']] = totalScore.get(i['name'], 0) + score
    
    ranking = sorted(totalScore.items(), key=lambda x: x[1], reverse=True)
    return ranking


