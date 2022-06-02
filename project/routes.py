from flask import render_template
from project import app
from .ranking import bestScore
from project import ranking

@app.route('/')
def index():
    header = ["Name", "Score"]
    return render_template('index.html', 
    header='Perspectum Assignment',headers=header,ranking=bestScore())
                        

