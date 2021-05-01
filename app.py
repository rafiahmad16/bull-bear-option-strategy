from flask import Flask, jsonify, render_template, session, request
from argparse import ArgumentParser

import requests
import time
from datetime import datetime
import json


app = Flask(__name__, template_folder='./')
app.secret_key = "87503O003d95U44369G3658b42A31288831d6lu94o60803P855"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-data', strict_slashes=False, methods=['GET'])
def getData():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers)
    if is_json(response.text) is False:
        print("error")
        print(response.status_code)
        print(response.text)
        return json.loads(response.text)
    return json.loads(response.text)

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
