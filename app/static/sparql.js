/**
 * Gestion des requêtes SPARQL
 */
async function executeSparql() {
    const endpoint = "http://localhost:10000/sparql";
    
    // Exemple de requête : Récupérer 5 films sur DBpedia
    const sparqlQuery = `
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?film ?description
        WHERE {
        ?film rdf:type dbo:Film ;
            dbo:description ?description .
        }
        LIMIT 5
    `;

    // Encodage de la requête pour l'URL
    const url = `${endpoint}?query=${encodeURIComponent(sparqlQuery)}`;

    try {
        console.log("Envoi de la requête SPARQL...");
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erreur réseau');
        
        const data = await response.json();
        console.log("Résultats :", data.results.bindings);
        
        // Affichage simple des résultats
        data.results.bindings.forEach(binding => {
            console.log(binding.label.value);
        });
    } catch (error) {
        console.error("Erreur lors de la requête SPARQL :", error);
    }
}

async function fetchGenresFromSPARQL() {
    const sparqlQuery = `
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX movie: <http://example.org/movie#>
        
        SELECT ?genre (COUNT(?film) as ?count)
        WHERE {
            ?film movie:hasGenre ?genre .
        }
        GROUP BY ?genre
        ORDER BY DESC(?count)
        LIMIT 10
    `;

    try {
        // Encoder la requête SPARQL pour l'URL
        const params = new URLSearchParams({ query: sparqlQuery });
        const response = await fetch(`/sparql?${params}`, {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data.results.bindings;

    } catch (error) {
        console.error("Erreur SPARQL:", error);
        return [];
    }
}

async function fetchFilmsAndGenre() {
    const sparqlQuery = `
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?film ?genre ?description ?starring ?director
        WHERE {
            ?film rdf:type dbo:Film .
    		OPTIONAL {?film dbo:genre ?genre. }
    		OPTIONAL {?film dbo:description ?description .}
    		OPTIONAL {?film dbo:starring ?starring .}
    		OPTIONAL {?film dbo:director ?director .}
        }
    `;

    try {
        // Encoder la requête SPARQL pour l'URL
        const params = new URLSearchParams({ query: sparqlQuery });
        const response = await fetch(`/sparql?${params}`, {
            method: "GET"
        });

        const data = await response.json();
        return data.results.bindings;

    } catch (error) {
        console.error("Erreur SPARQL:", error);
        return [];
    }
}