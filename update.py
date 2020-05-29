import requests
from bs4 import BeautifulSoup

url = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
html = requests.get(url)
code = BeautifulSoup(html.text, "html.parser")
with open('covid.txt', 'w') as f:
    code = code.text.split('\n')
    for line in code:
        if line != '\n':
            print(line.rstrip(), file = f)
