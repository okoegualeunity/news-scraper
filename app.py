from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Use environment variable if set, else fallback to your key (for testing only)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY") or "2144235fe6f141e0810be96db9fb3229"

@app.route('/')
def index():
    return "✅ NewsAPI Flask app is running and ready!"

@app.route('/scrape-news')
def scrape_news():
    try:
        url = f'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        articles = []
        for item in data.get('articles', []):
            articles.append({
                'title': item['title'],
                'url': item['url']
            })

        return jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': articles
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ✅ Required for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
