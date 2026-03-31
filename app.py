from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route ping (pour UptimeRobot - évite la mise en veille)
@app.route('/ping')
def ping():
    return "pong", 200

# Route recherche de jeux
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # Exemple avec l'API RAWG (gratuite)
    API_KEY = "TON_API_KEY_RAWG"
    url = f"https://api.rawg.io/api/games?key={API_KEY}&search={query}&page_size=10"
    
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
