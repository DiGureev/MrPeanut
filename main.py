from flask import Flask
import json
import os
from script import getOpengraphData

app = Flask(__name__)

def readFile(username):
    result = {}
    with open(f"./{username}.json","r") as f:
        result = json.load(f)
    return result

def writeFile(username, object):
    with open(f"./{username}.json", "w") as f:
        json.dump(object, f)
    return

@app.route('/favicon.ico')
def checkFav():
    return {}, 200

@app.route("/<username>")
def home(username):
    if os.path.exists(f"./{username}.json"):
        print("Exist")
        result = readFile(username)
    else:
        print("Does not exist")
        result  = getOpengraphData(username)
        writeFile(username, result)
    return result, 200

if __name__ == "__main__":
    app.run(debug=True)
