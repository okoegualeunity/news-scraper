from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Pulls port from Render
    print(f"Running on port {port}")          # Optional: debug message
    app.run(host='0.0.0.0', port=port)        # Binds to 0.0.0.0
