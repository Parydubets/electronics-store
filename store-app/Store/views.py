from Store import app
from flask import render_template
import os

@app.route('/')
@app.route('/clients')
def clients():
    print(os.path)
    #return "HALO"
    return render_template('clients.html')