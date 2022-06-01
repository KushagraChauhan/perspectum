'''
    This is the main file of the Flask app
'''
from email import header
from flask import Flask, jsonify, render_template
import logging, json
from flask_paginate import Pagination, get_page_parameter
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

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
    try:
        for item in json_list:
            subs = item.get("submissions", [])
            if isinstance(subs, list):
                subs.sort(key=lambda x: x.get("score", 0), reverse=True)
    except:
        logger.error("We have a problem, sir %s", exec_info=1)

sort_submissions_of_items(inputData)

header = ["#", "Name", "Score"]
@app.route('/')
def index():
    page, per_page, offset = 1, 10, 0
    rankings = bestScore()
    #pagination_rankings = bestScore(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(rankings),
                            css_framework='bootstrap4')
    # pagination = Pagination(page=1, total=len(rankings), search=False, record_name='users', per_page=10)
    return render_template('index.html', 
    header='Perspectum Assignment',headers=header,rankings=bestScore(),
                           page=page,
                           per_page=10,
                           pagination=pagination,)

def bestScore():
    totalScore = {}
    try:
        for i in inputData:
            score = 0
            if len(i['submissions']) >= 3:
                for j in range(len(i['submissions'])):
                    score += i['submissions'][j]['score']
                    if j > 22:
                        break
                totalScore[i['name']] = totalScore.get(i['name'], 0) + score
                           
    except:
        logger.error("We have a problem sir, %s",exec_info=1)

    ranking = sorted(totalScore.items(), key=lambda x: x[1], reverse=True)
    return ranking


if __name__ == "__main__":
    app.run(debug=True)
