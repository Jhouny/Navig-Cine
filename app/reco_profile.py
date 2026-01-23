from SPARQLWrapper import SPARQLWrapper, JSON
import heapq
from openai import OpenAI
from random import random
import utils

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

def get_reco(profil, query ="default", test=False, randomfactor = 0):

    print(f'-------- get_reco\nprofil envoyé : {profil}')
    genres = profil.get("genres")
    realisateurs = profil.get("realisateurs")
    acteurs = profil.get("acteurs")

    # concatenate, add prefix and replace splace with underlines
    string_de_genres = ", ".join(f"<http://dbpedia.org/resource/{g}>".replace(" ", "_" ) for g in genres.keys())
    string_de_realisateurs = ", ".join(f"<http://dbpedia.org/resource/{g}>".replace(" ", "_" ) for g in realisateurs.keys())
    string_dacteurs = ", ".join(f"<http://dbpedia.org/resource/{g}>".replace(" ", "_" ) for g in acteurs.keys())
  
    if (query == "default"):
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>

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
        #print(f'---this is not a test\n---query : \n{query}')
        sparql = SPARQLWrapper("http://127.0.0.1:7201/repositories/Gdb-Navig-Cine")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        #print(f'---relts : \n{results["results"]["bindings"]}')
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
            #acteur = acteur.replace("http://dbpedia.org/resource/", "dbr:" )
            #print(f'{utils.removePathPrefix(acteur).replace("_"," ")} in {profil.get("acteurs").keys()}')
            if(utils.removePathPrefix(acteur).replace('_',' ') in profil.get("acteurs").keys()):
                score += (profil.get("acteurs").get(utils.removePathPrefix(acteur).replace("_"," ")) + randomfactor*random())

        for real in liste_de_reals:
            #real = real.replace("http://dbpedia.org/resource/", "dbr:" )
            if(utils.removePathPrefix(real).replace('_',' ') in profil.get("realisateurs").keys()):
                score += (profil.get("realisateurs").get(utils.removePathPrefix(real).replace("_"," ")) + randomfactor*random())

        for genre in liste_de_genres:
            #genre = genre.replace("http://dbpedia.org/resource/", "dbr:" )
            if(utils.removePathPrefix(genre).replace('_',' ') in profil.get("genres").keys()):
                score += (profil.get("genres").get(utils.removePathPrefix(genre).replace("_"," ")) + randomfactor*random())
        
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

    # Remove dbpedia prefixes
    for r in res:
        r["Film"] = r["Film"].replace("http://dbpedia.org/resource/", "")
        r["Film"] = r["Film"].replace("dbr:", "")
        r["Realisateurs"] = [real.replace("http://dbpedia.org/resource/", "") for real in r["Realisateurs"]]
        r["Realisateurs"] = [real.replace("dbr:", "") for real in r["Realisateurs"]]
        r["Acteurs"] = [actor.replace("http://dbpedia.org/resource/", "") for actor in r["Acteurs"]]
        r["Acteurs"] = [actor.replace("dbr:", "") for actor in r["Acteurs"]]
        r["Genres"] = [genre.replace("http://dbpedia.org/resource/", "") for genre in r["Genres"]]
        r["Genres"] = [genre.replace("dbr:", "") for genre in r["Genres"]]
    
    # Replace underlines with spaces for better readability
    for r in res:
        r["Film"] = r["Film"].replace("_", " ")
        r["Realisateurs"] = [real.replace("_", " ") for real in r["Realisateurs"]]
        r["Acteurs"] = [actor.replace("_", " ") for actor in r["Acteurs"]]
        r["Genres"] = [genre.replace("_", " ") for genre in r["Genres"]]
    
    # Drop empty items from lists
    for r in res:
        r["Realisateurs"] = [real for real in r["Realisateurs"] if real not in ["", "N/A"]]
        r["Acteurs"] = [actor for actor in r["Acteurs"] if actor not in ["", "N/A"]]
        r["Genres"] = [genre for genre in r["Genres"] if genre not in ["", "N/A"]]
        
    return res


if __name__ == "__main__":
    # Lancement de la requête
    profil = {
    'Films': {'Shadow of Heroes': 1, 'Vlastně se nic nestalo': 1, 'Earth to America': 1, 'Fred: The Movie': 1, 'Goli Soda Rising': 1, 'Final Run': 1, 'Harlan County War': 1, 'Beaches': 1, 'Fascist Legacy': 1, 'Boom Bust Boom': 1}, 
    'genres': {'Drama': 2, 'Comedy': 2, 'Action_film': 2, 'Drama_(film_and_television)': 2, 'Documentary_film': 2}, 
    'realisateurs': {'Clay Weiner': 1}, 
    'acteurs': {'John Cena': 1, 'Lucas Cruikshank': 1, 'Jake Weary': 1, 'Pixie Lott': 1, 'Jennette McCurdy': 1, 'Oscar Nunez': 1, 'Siobhan Fallon Hogan': 1}
    }
    requete_naturelle = "les films réalisés par Blair Treu"
    df_reco = get_reco(profil, randomfactor=5)
    print(df_reco)