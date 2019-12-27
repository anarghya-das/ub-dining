from flask import Flask, request
import requests
import json

app = Flask(__name__)


@app.route('/')
def homepage():
    return "Hello, this shit works!"


@app.route('/ub_locations', methods=['POST'])
def alexa():
    data = request.json
    reso = {}
    inner = {"version": "1.0", "sessionAttributes": {}}
    res = {"shouldEndSession": False, "type": "_DEFAULT_RESPONSE"}
    out = {"type": "PlainText"}
    welcome_message = 'Hello, would you like to know where you can eat at UB? Ask about where you could eat by date and I will tell you.'
    out["text"] = welcome_message
    res["outputSpeech"] = out
    inner["response"] = res
    reso["body"] = inner
    outp = json.dumps(reso)
    print(outp)
    return outp


if __name__ == "__main__":
    app.run(debug=True)
