import requests
import random as r

def removePathPrefix(uri):
    prefixe = "http://dbpedia.org/resource/"

    if uri.startswith(prefixe):
        return uri[len(prefixe):]
    
    return uri

def convertSPARQLOutputToDico(results):
    print("Converting SPARQL output to dictionary...")
    
    dico_genres_films = {}
    dico_films_descriptions = {}
    dico = {"results": {"bindings": {"genres": dico_genres_films, "films": dico_films_descriptions}}}

    # The film name is unique, we must join information from multiple rows
    for row in results["results"]["bindings"]:
        film = row.get("film", {}).get("value", "N/A")
        genre = row.get("genre", {}).get("value", "N/A")
        description = row.get("description", {}).get("value", "N/A")
        starring = row.get("starring", {}).get("value", "N/A")
        director = row.get("director", {}).get("value", "N/A")

        film_clean = removePathPrefix(film)
        genre_clean = removePathPrefix(genre)
        description_clean = removePathPrefix(description)
        starring_clean = removePathPrefix(starring)
        director_clean = removePathPrefix(director)

        # Fix naming formats for better readability
        film_clean = film_clean.replace("_", " ")
        description_clean = description_clean.replace("_", " ")
        starring_clean = starring_clean.replace("_", " ")
        director_clean = director_clean.replace("_", " ")

        # Remove parentheses from film titles
        if "(" in film_clean:
            film_clean = film_clean.split("(")[0].strip()

        # Merge duplicates: if film already exists, update info
        if film_clean in dico_films_descriptions:
            if starring_clean not in dico_films_descriptions[film_clean]["starring"]:
                dico_films_descriptions[film_clean]["starring"].append(starring_clean)
            if dico_films_descriptions[film_clean]["director"] == "N/A" and director_clean != "N/A":
                dico_films_descriptions[film_clean]["director"] = director_clean
            if dico_films_descriptions[film_clean]["description"] == "N/A" and description_clean != "N/A":
                dico_films_descriptions[film_clean]["description"] = description_clean
        else:
            dico_films_descriptions[film_clean] = {
                "description": description_clean,
                "starring": [starring_clean],
                "director": director_clean,
            }
        dico_genres_films.setdefault(genre_clean, []).append(film_clean)

    return dico

def keepTopNResults(results, N):

    # Garder uniquement les 5 genres avec les plus de films
    sorted_genres = sorted(results["results"]["bindings"]["genres"].items(), key=lambda item: len(item[1]), reverse=True)
    idx = r.randint(0, 2*N)
    topN_genres = dict()

    for i in range (0, N):
        topN_genres[sorted_genres[i+idx][0]] = sorted_genres[i+idx][1]
    
    results["results"]["bindings"]["genres"] = topN_genres

    return results

def get_movie_data_omdb(movie_title, api_key):
    # L'URL de base d'OMDb
    url = "http://www.omdbapi.com/"

    # Paramètres : 't' pour le titre, 'apikey' pour votre clé
    params = {
        "t": movie_title,
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # OMDb renvoie toujours 'Response': 'True' ou 'False'
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "poster_url": data.get("Poster"), # L'URL de l'image
                "imdb_id": data.get("imdbID")
            }
        else:
            print(f"Erreur OMDb pour le film \'{movie_title}\': {data.get('Error')}")
            return None
            
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        return None
