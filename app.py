from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

RAWG_API_KEY = os.environ.get("Samouneji")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return "pong", 200

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={query}&page_size=10"
    
    response = requests.get(url)
    data = response.json()
    
    games = []
    for game in data.get('results', []):
        games.append({
            'name': game['name'],
            'image': game.get('background_image', ''),
            'rating': game.get('rating', 0),
            'released': game.get('released', 'N/A'),
            'platforms': [p['platform']['name'] for p in game.get('platforms', [])]
        })
    
    return jsonify(games)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
