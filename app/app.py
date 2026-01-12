from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON, RDFXML, GET

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/sparql', methods=['GET'])
def query_sparql():
    print("Received SPARQL query request")
    # Récupération de la requête passée en paramètre d'URL
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    sparql = SPARQLWrapper("http://10.56.62.206:7200/repositories/Gdb-Navig-Cine")
    sparql.setMethod(GET)
    sparql.setQuery(query)
    sparql.setReturnFormat(RDFXML)

    try:
        results = sparql.query()
        print("results:", results)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )
    print("Server is running on http://localhost:10000")
