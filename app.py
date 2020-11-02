from flask import Flask, jsonify, render_template, session, request
from argparse import ArgumentParser

import requests
import time
from datetime import datetime
import json


app = Flask(__name__,template_folder='./')
app.secret_key = "87503O003d95U44369G3658b42A31288831d6lu94o60803P855"

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get-data',strict_slashes=False,methods=['GET'])
def getData():
    returnDic = {}
    data = getNSEData()
    returnDic['expires'] = data['records']['expiryDates']
    expiry = request.args.get('expiry')
    print(expiry)
    if expiry is None:
        expiry = returnDic['expires'][0]
    expiryData = []
    for d in data['records']['data']:
        if d['expiryDate'] == expiry:
            expiryData.append(d)
        
    returnDic['symbol'] = 'NIFTY'
    returnDic['data'] = expiryData
    returnDic['currentPrice'] = expiryData[0]['CE']['underlyingValue']
    return jsonify(returnDic)




def getNSEData():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    if session.get('headers') is None:
        print("adding new headers")
        headers = getNSECookies()
        session['headers'] = headers
    headers = session.get('headers')
    response = requests.request("GET", url, headers=headers)
    if is_json(response.text) is False:
        print(response.text)
        print("Removing old headers")
        session.pop('headers')
        time.sleep(10)
        getNSEData()
    return json.loads(response.text)
    
    


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def getNSECookies():
    url = app.config['url']
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers)
    cookies_dic = response.cookies.get_dict()
    print(cookies_dic)
    cookies_dic.update(headers)
    return cookies_dic



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-url')
    args = parser.parse_args()
    if args.url is None:
        print("-url <url from nseindia.com=>Market Data=>Derivative Market >")
    else:
        app.config['url'] = args.url
        app.run(host='127.0.0.1',port=9000,debug=True)

    #strike = int(args.strike)
    #app.config['url'] = '%.2f' % strike
    
