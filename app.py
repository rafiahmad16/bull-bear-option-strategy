from flask import Flask, jsonify, render_template
from argparse import ArgumentParser

import requests
import time
from datetime import datetime
import json


app = Flask(__name__,template_folder='./')

EXPIRY_DATES = [22, 29]

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get-data',strict_slashes=False,methods=['GET'])
def getData(expiry = None):
    returnDic = {}
    data = getNSEData()
    if 'status' in data:
        return data
    returnDic['expires'] = data['records']['expiryDates']
    if expiry is None:
        expiry = returnDic['expires'][0]
    expiryData = []
    if 'records' in data:
        for d in data['records']['data']:
            if d['expiryDate'] == expiry:
                expiryData.append(d)
        
    returnDic['symbol'] = 'NIFTY'
    returnDic['data'] = expiryData
    returnDic['currentPrice'] = expiryData[0]['CE']['underlyingValue']
    return jsonify(returnDic)




def getNSEData():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = getNSECookies()
    response = requests.request("GET", url, headers=headers)
    if is_json(response.text) is False:
        print(response.text)
        return {'status': False, 'message': 'Invalid response in api'}
    return json.loads(response.text)
    


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def getNSECookies():
    currenttimestamp = int(time.time())
    current_time = datetime.fromtimestamp(currenttimestamp)
    currentDate = current_time.day
    currentMonth = current_time.month
    currentYear = current_time.year
    expiryDate = EXPIRY_DATES[0]
    for d in range(currentDate,32):
        if d in EXPIRY_DATES:
            expiryDate = d
            break
    url = "https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY&identifier=OPTIDXNIFTY"+str(expiryDate)+"-"+str(currentMonth)+"-"+str(currentYear)+"CE"+str(app.config['strike'])
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers)
    cookies_dic = response.cookies.get_dict()
    cookies_dic.update(headers)
    return cookies_dic







if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-strike')
    args = parser.parse_args()
    strike = int(args.strike)
    app.config['strike'] = '%.2f' % strike
    app.run(host='127.0.0.1',port=1234,debug=True)
