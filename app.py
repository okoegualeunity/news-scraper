from flask import Flask, jsonify, make_response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

app = Flask(__name__)

# Set custom headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/')
def index():
    return "✅ Flask app is running and responding!"

@app.route('/scrape-news')
def scrape_news():
    try:
        base_url = 'https://www.bbc.com'
        tech_url = urljoin(base_url, '/news/technology')

        response = requests.get(tech_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        for item in soup.select('a.gs-c-promo-heading[href]'):
            title = item.get_text(strip=True)
            link = item['href']

            if not link.startswith('http'):
                link = urljoin(base_url, link)

            articles.append({
                'title': title,
                'url': link
            })

        resp = jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': articles
        })
        resp.headers['Cache-Control'] = 'public, max-age=300'
        return resp

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ✅ Use this for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
