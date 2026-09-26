from flask import Flask, render_template
from flask import request
import pickle
import os
app = Flask(__name__)

if not os.path.isfile("database.pkl"):
    DATABASE = {}
else:
    with open("database.pkl", "rb") as f:
        DATABASE = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        word = result['word']
        meaning = result['meaning']
        DATABASE[word] = meaning

        try:
            with open("database.pkl", "wb") as f:
                pickle.dump(DATABASE, f)
        except Exception as e:
            print(e)


    return render_template("on_submit.html", result = result)

@app.route('/revise',methods = ['POST', 'GET'])
def revise():
    return render_template("revise.html", db = DATABASE)


if __name__ == "__main__":
    app.run(port=5000)
