from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON, GET

from reco_profile import get_reco
from utils import convertSPARQLOutputToDico, keepTopNResults, get_movie_data_omdb
from dotenv import load_dotenv
import os

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
base_url = os.getenv("BASE_URL", "localhost:7200")
print("Using base URL for SPARQL endpoint:", base_url)

recommendations_cache = {}  # Dictionnaire pour stocker les recommandations en cache

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommendations")
def recommendations():
    uid = request.args.get('uid')
    recommandations = recommendations_cache.get(uid, [])
    return render_template("recommendations/index.html", recommandations=recommandations)

@app.route('/sparql', methods=['GET'])
def query_sparql():
    # Récupération de la requête passée en paramètre d'URL
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    sparql = SPARQLWrapper(f"http://{base_url}/repositories/Gdb-Navig-Cine")
    sparql.setMethod(GET)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        convertedResults = convertSPARQLOutputToDico(results)
        topN = 5
        results_limited = keepTopNResults(convertedResults, topN)

        return jsonify(results_limited), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/reco', methods=['POST'])
def get_recommandations():
    try:
        user_profil = request.json.get('profil')
        print("Received user profile:", user_profil)
        uid = request.json.get('uid')
        recommendations = get_reco(user_profil, query="default", test=False,randomfactor=5)
        recommendations_cache[uid] = recommendations  # Stockage des recommandations dans le cache
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/poster', methods=['GET'])
def get_poster():
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "No movie title provided"}), 400

    movie_data = get_movie_data_omdb(movie_title, OMDB_API_KEY)
    poster_url = movie_data.get("poster_url") if movie_data else None
    if poster_url:
        return jsonify(poster_url), 200
    else:
        return jsonify({"error": "Poster not found"}), 404

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )
    print("Server is running on http://localhost:10000")
