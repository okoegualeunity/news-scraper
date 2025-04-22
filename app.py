from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

app = Flask(__name__)

# Set custom headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

@app.route('/')
def index():
    return "✅ Flask app is running and responding!"

@app.route('/scrape-news')
def scrape_news():
    try:
        url = 'https://www.bbc.co.uk/news/topics/c50znx8v122t'
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # Select headline anchors
        items = soup.select('a.gs-c-promo-heading')

        for item in items:
            title = item.get_text(strip=True)
            link = item.get('href')

            # Convert relative URL to full
            if link and not link.startswith('http'):
                link = urljoin('https://www.bbc.co.uk', link)

            if title and link:
                articles.append({
                    'title': title,
                    'url': link
                })

        return jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': articles
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ✅ Required for Render (port binding)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
