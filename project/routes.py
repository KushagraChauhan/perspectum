from flask import render_template
from project import app
from .ranking import bestScore


@app.route('/rankings')
def index():
    header = ["Name", "Score"]
    return render_template('index.html', 
    header='Perspectum Assignment',headers=header,rankings=bestScore())
                        

