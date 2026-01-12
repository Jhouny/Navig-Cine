from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )
    print("Server is running on http://localhost:5000")

@app.route('/sparql', methods=['GET'])
def query_sparql():
    print("Received SPARQL query request")
    # Récupération de la requête passée en paramètre d'URL
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    sparql = SPARQLWrapper("http://10.56.62.206:7200")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500