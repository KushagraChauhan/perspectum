'''
    This is the main file of the Flask app
'''

from copy import deepcopy
from flask import Flask, jsonify
import logging, json

#Intializing the Flask app
app = Flask(__name__)
dataset = 'scores.json'

# Initialzing logger for better debugging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,format='%(asctime)s: %(levelname)s: %(message)s')

# Load the JSON Dataset
with open(dataset, 'r', encoding='utf-8') as data_file:    
    inputData = json.load(data_file)

# Sort the JSON on the basis of score
def sort_submissions_of_items(json_list):
    for item in json_list:
        subs = item.get("submissions", [])
        if isinstance(subs, list):
            subs.sort(key=lambda x: x.get("score", 0), reverse=True)

sort_submissions_of_items(inputData)

@app.route('/')
def index():
    return 'App is running'


@app.route('/names')
def getNames():
    names = []
    for i in inputData:
        names.append(i['name'])
    return jsonify(names)

'''
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
    Sum of best 24 submissions
'''
@app.route('/ranks')
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
                logger.info(j)
                if j > 22:
                    break
            totalScore[i['name']] = totalScore.get(i['name'], 0) + score
    return jsonify(totalScore)

if __name__ == "__main__":
    app.run(debug=True)
