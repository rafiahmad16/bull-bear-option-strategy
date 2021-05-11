from flask import Flask, render_template, request

import requests
from datetime import datetime
import json


app = Flask(__name__, template_folder='./')
app.secret_key = "87503O003d95U44369G3658b42A31288831d6lu94o60803P855"


@app.route('/')
def hello_world():
    with open('./stocks.json') as json_file:
        stocks = json.load(json_file)
    return render_template('index.html', stocks=stocks)


@app.route('/get-data', strict_slashes=False, methods=['GET'])
def getData():
    selected_stock = request.args.get('selected_stock')
    
    if (selected_stock == "NIFTY" or selected_stock == "BANKNIFTY"):
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={selected_stock}"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={selected_stock}"     

    url_oc = "https://www.nseindia.com/option-chain"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'
    }
    session = requests.Session()
    request_cookies = session.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request_cookies.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    if is_json(response.text) is False:
        print("error")
        print(response.status_code)
        print(response.text)
        return json.loads(response.text)
    print("Successs")
    return json.loads(response.text)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
