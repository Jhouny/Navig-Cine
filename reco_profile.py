#from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

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
        sparql = SPARQLWrapper("https://fr.dbpedia.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    else :
        results = {
                    "results": {
                        "bindings": [
                        {"film":{"value":"dbr:Film_1"},
                        "directors":{"value":"dbr:David_Frankel"},
                        "actors":{"value":"dbr:Anne_Hathaway"},
                        "genres":{"value":"dbr:Fantasy_comedy"}},
                        {"film":{"value":"dbr:Film_2"},
                        "directors":{"value":"dbr:James_Cameron"},
                        "actors":{"value":"dbr:Tom_Cruise, dbr:Anne_Hathaway, dbr:Leonardo_Di_Caprio"},
                        "genres":{}},
                        {"film":{"value":"dbr:Film_3"},
                        "directors":{"value":"dbr:David_Frankel"},
                        "actors":{"value":"dbr:Meryl_Streep"},
                        "genres":{"value":"dbr:OtherGenre"}}
                        ]
                    }
                    }
    
    # Requête et transformation du résultats en pandas dataframe
    data = []
    for result in results["results"]["bindings"]:
        score = 0
        liste_dacteurs = result.get("actors", {}).get("value", "N/A").split(", ")
        liste_de_reals = result.get("directors", {}).get("value", "N/A").split(", ")
        liste_de_genres = result.get("genres", {}).get("value", "N/A").split(", ")

        
        for acteur in liste_dacteurs:
            if(acteur in profil.get("acteurs").keys()):
                score += profil.get("acteurs").get(acteur)

        for real in liste_de_reals:
            if(real in profil.get("realisateurs").keys()):
                score += profil.get("realisateurs").get(real)

        for genre in liste_de_genres:
            if(genre in profil.get("genres").keys()):
                score += profil.get("genres").get(genre)
        
        data.append({#possibilité de faire une prior queue ? 
            "Film": result.get("film", {}).get("value", "N/A"),
            "Realisateurs" : liste_de_reals,
            "Acteurs": liste_dacteurs,
            "Genres": liste_de_genres,
            "Score": score
        })
    return pd.DataFrame(data).sort_values("Score", ascending=False)

# Lancement de la requête
profil = {'Films' : {},'genres' : {'dbr:Fantasy_comedy':10}, 'realisateurs' : {'dbr:David_Frankel' : 2, 'dbr:James_Cameron' : 1},'acteurs' : {'dbr:Anne_Hathaway':1, 'dbr:Tom_Cruise':1, 'dbr:Meryl_Streep':4}}
df_reco = get_reco(profil,test=True)
print(df_reco.head())