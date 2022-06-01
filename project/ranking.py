import logging, json

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

