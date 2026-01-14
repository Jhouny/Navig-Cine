from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_reco(profil):

    genres = profil.get("genres")
    realisateurs = profil.get("realisateurs")
    acteurs = profil.get("acteurs")

    string_de_genres = ", ".join(genres.keys())
    string_de_realisateurs = ", ".join(realisateurs.keys())
    string_dacteurs = ", ".join(acteurs.keys())
    
    sparql = SPARQLWrapper("https://fr.dbpedia.org/sparql")
    
    # Requête complexe : Albums, dates et genres
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
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    # Requête et transformation du résultats en pandas dataframe
    data = []
    for result in results["results"]["bindings"]:
        score = 0
        liste_dacteurs = result.get("actors", {}).get("value", "N/A").split(", ")
        liste_de_reals = result.get("directors", {}).get("value", "N/A").split(", ")
        liste_de_genres = result.get("genres", {}).get("value", "N/A").split(", ")

        #todo : calculer score
        
        data.append({#possibilité de faire une prior queue ? 
            "Film": result.get("film", {}).get("value", "N/A"),
            "Realisateurs" : liste_de_reals,#gerer liste
            "Acteurs": liste_dacteurs,#gerer liste
            "Genres": liste_de_genres,#gerer liste
            "Score": score
        })
    return pd.DataFrame(data)

# Lancement de la requête
profil = {'Films' : {},'Genre' : {'Drama' : 3, 'Fantaisie' : 2}, 'Réalisateurs' : {'Spielberg' : 3},'Acteurs' : {}}
df_music = query_dbpedia(profil)
df_music.head()