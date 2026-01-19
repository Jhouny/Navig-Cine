from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON, RDFXML, GET

from reco_profile import get_reco
from utils import convertSPARQLOutputToDico

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/sparql', methods=['GET'])
def query_sparql():
    #print("Received SPARQL query request: ", request.args)
    
    # Récupération de la requête passée en paramètre d'URL
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    sparql = SPARQLWrapper("http://10.56.62.206:7200/repositories/Gdb-Navig-Cine")
    sparql.setMethod(GET)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        print(results)
        convertedResults = convertSPARQLOutputToDico(results)

        return jsonify(convertedResults), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/reco', methods=['GET', 'POST'])
def get_recommandations():
    try:
        # print("Received recommendation request: ", request.json)
        # print("=================")
        user_profil = request.json.get('profil')
        # print("User profil: ", user_profil)
        # print("=================")

        # Appel de votre fonction Python locale
        recommendations = get_reco(user_profil, query ="default", test=True)
        # print("Recommendations: ", recommendations)
        
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )
    print("Server is running on http://localhost:10000")
