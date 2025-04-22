from flask import Flask, jsonify, make_response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        
        # Add timeout and headers to the request
        response = requests.get(tech_url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # More specific selector to get proper news items
        for item in soup.select('a.gs-c-promo-heading[href]'):
            title = item.get_text(strip=True)
            link = item['href']
            
            # Ensure absolute URLs
            if not link.startswith('http'):
                link = urljoin(base_url, link)
                
            articles.append({
                'title': title,
                'url': link
            })

        # Create response with cache control headers
        resp = jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': articles
        })
        resp.headers['Cache-Control'] = 'public, max-age=300'  # 5 minute cache
        return resp

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True)
