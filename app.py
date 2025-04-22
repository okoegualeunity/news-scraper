from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Secure way to use the key (env variable preferred)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY") or "e95461392a8e4d5c96016282fc4d25d5"

@app.route('/')
def index():
    return "✅ Flask app using NewsAPI is running!"

@app.route('/scrape-news')
def scrape_news():
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}'
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
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ✅ Port binding for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
