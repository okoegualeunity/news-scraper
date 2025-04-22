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

@app.route('/scrape-news')
def scrape_news():
    try:
        url = 'https://news.ycombinator.com/'
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # ⚠️ TEMP: See what Render is getting
        return response.text

    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 500


# ✅ Required for Render (port binding)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
