'''
    This is the main file of the Flask app
'''

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
@app.route('/ranks')
def getScores():
    totalScore = {}
    for i in inputData:
        score = 0
        for j in i['submissions']:
            score += j['score']
        logger.info(score)
        totalScore[i['name']] = totalScore.get(i['name'], 0) + score
    
    return jsonify(totalScore)


if __name__ == "__main__":
    app.run(debug=True)
