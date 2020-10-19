# Bull Call Spread and Bear Put Spread Option Strategy

![alt sample](https://github.com/rafiahmad16/bull-bear-option-strategy/blob/master/sample.png?raw=true)

# About

This is a simple flask application which  scrap [nseindia](https://www.nseindia.com/market-data/equity-derivatives-watch) option chain(Only NIFTY) data and show the bull call spread and bear put spread in tabular format.

It helps traders to select the best strike price to choose among the strike prices at which derivative can be bought and short-selling

I am still working on this application to improve and optimize. If you find any sort of error please report an issue.

Feel free to fork, it is welcome for any suggestion and ideas for the improvement of the application.

# Installation process

## using conda 

 `conda env create -f environment.yml`

## using pip

 `pip install -r requirements.txt`
# How to run

 `python app.py -strike 11800`
and then open [http://localhost:1234](http://localhost:1234) in your browser.
