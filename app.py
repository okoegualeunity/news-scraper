from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Flask app is running and responding!"

@app.route('/scrape-news')
def scrape_news():
    url = 'https://www.bbc.com/news/technology'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.select('a.gs-c-promo-heading'):
        title = item.get_text()
        link = item['href']
        if link.startswith('/'):
            link = 'https://www.bbc.com' + link
        articles.append({'title': title, 'url': link})

    return jsonify(articles)
