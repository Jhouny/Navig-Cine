from SPARQLWrapper import SPARQLWrapper, JSON
import heapq
from openai import OpenAI

def requete_sparql(requete_naturelle):
        
    # Initialize the client
    client = OpenAI(
        base_url="https://ollama-ui.pagoda.liris.cnrs.fr/api",  
        api_key="sk-35729c1f15074008972ee602959d9f7b",         #   (go to profile - bottom left, account)
    )

    # Call the 70B model
    response = client.chat.completions.create(
        model="llama3:70b",
        messages=[
            {"role": "system", "content": "Tu es un traducteur de requêtes plein texte vers SPARQL. \
             Tu utilises un graphe qui contient uniquement ?film dbo:director ?director, ?film dbo:starring ?actor, ?film dbo:genre ?genre et ?film dbo:description ?description. Tu connais des éléments de modèle suivant : <http://dbpedia.org/resource/Comedy>. La requete doit repourner : ?film l'url du film, ?directors la liste des uri des realisateurs séparés par une virgule et un espace, ?genres la liste des uri des genres séparés par une virgule et un espace et ?actors liste des uri des acteurs séparés par une virgule et un espace. Tu ne dois répondre qu'en SPARQL, aucun texte, aucune explication en sus."},
            {"role": "user", "content": requete_naturelle}
        ],
        temperature=0.7
    )

    requete_sparql = response.choices[0].message.content
    return requete_sparql

def get_reco_par_requete_naturelle(profil, requete_naturelle):
    ma_requete_sparql = requete_sparql(requete_naturelle)
    reco = get_reco(profil, query =ma_requete_sparql)
    return reco

def get_reco(profil, query ="default", test=False):

    genres = profil.get("genres")
    realisateurs = profil.get("realisateurs")
    acteurs = profil.get("acteurs")

    string_de_genres = ", ".join(genres.keys())
    string_de_realisateurs = ", ".join(realisateurs.keys())
    string_dacteurs = ", ".join(acteurs.keys())

  
    if (query == "default"):
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>

        SELECT ?film 
        (GROUP_CONCAT(DISTINCT ?director; separator=", ") AS ?directors) 
        (GROUP_CONCAT(DISTINCT ?genre; separator=", ") AS ?genres) 
        (GROUP_CONCAT(DISTINCT ?actor; separator=", ") AS ?actors)
        WHERE {{{{ 
        ?film dbo:director ?director .
        FILTER(?director IN({string_de_realisateurs})) 
        }}UNION{{
            ?film dbo:starring ?actor.
            FILTER(?actor IN ({string_dacteurs})) 
        }}UNION{{
            ?film dbo:genre ?genre.
            FILTER ( ?genre IN ({string_de_genres}))
        }}}}
        GROUP BY ?film
        """
    
    if (not test) :
        sparql = SPARQLWrapper("http://127.0.0.1:7201/repositories/Gdb-Navig-Cine") #chez jhouny : 10.56.62.206:7200
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    else :
        results = {
                    "results": {
                        "bindings": [
                            {
                                "film":{"value":"dbr:Film_1"},
                                "directors":{"value":"dbr:David_Frankel"},
                                "actors":{"value":"dbr:Anne_Hathaway"},
                                "genres":{"value":"dbr:Fantasy_comedy"}
                            },
                            {
                                "film":{"value":"dbr:Film_2"},
                                "directors":{"value":"dbr:James_Cameron"},
                                "actors":{"value":"dbr:Tom_Cruise, dbr:Anne_Hathaway, dbr:Leonardo_Di_Caprio"},
                                "genres":{}
                            },
                            {
                                "film":{"value":"dbr:Film_3"},
                                "directors":{"value":"dbr:David_Frankel"},
                                "actors":{"value":"dbr:Meryl_Streep"},
                                "genres":{"value":"dbr:OtherGenre"}
                            }
                        ]
                    }
                }
    
    # Requête et transformation du résultats en pandas dataframe
    data_priorQ = []
    i= 0
    for result in results["results"]["bindings"]:
        score = 0
        liste_dacteurs = result.get("actors", {}).get("value", "N/A").split(", ")
        liste_de_reals = result.get("directors", {}).get("value", "N/A").split(", ")
        liste_de_genres = result.get("genres", {}).get("value", "N/A").split(", ")

        
        for acteur in liste_dacteurs:
            acteur = acteur.replace("http://dbpedia.org/resource/", "dbr:" )
            if(acteur in profil.get("acteurs").keys()):
                score += profil.get("acteurs").get(acteur)

        for real in liste_de_reals:
            real = real.replace("http://dbpedia.org/resource/", "dbr:" )
            if(real in profil.get("realisateurs").keys()):
                score += profil.get("realisateurs").get(real)

        for genre in liste_de_genres:
            genre = genre.replace("http://dbpedia.org/resource/", "dbr:" )
            if(genre in profil.get("genres").keys()):
                score += profil.get("genres").get(genre)
        
        heapq.heappush(data_priorQ, (-score, i, {
            "Film": result.get("film", {}).get("value", "N/A"),
            "Realisateurs" : liste_de_reals,
            "Acteurs": liste_dacteurs,
            "Genres": liste_de_genres,
            "Score": score
        }))
        i +=1

    res = []
    while data_priorQ :
        task = heapq.heappop(data_priorQ)[2]
        res.append(task)
            
        
    return res


if __name__ == "__main__":
    # Lancement de la requête
    profil = {
        'Films' : {},
        'genres' : {'dbr:Science_fiction':10}, 
        'realisateurs' : {'dbr:David_Frankel' : 2, 
                        'dbr:James_Cameron' : 1, 
                        'dbr:Christopher_Nolan' : 11},
        'acteurs' : {'dbr:Anne_Hathaway':1, 
                    'dbr:Tom_Cruise':1, 
                    'dbr:Meryl_Streep':4, 
                    'dbr:Jessica_Tuck' : 2}
            }
    requete_naturelle = "les films réalisés par Blair Treu"
    df_reco = get_reco_par_requete_naturelle(profil, requete_naturelle)
    print(df_reco)