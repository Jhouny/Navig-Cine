import requests

from dotenv import load_dotenv
import os

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

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

    for row in results["results"]["bindings"]:
        film = row.get("film", {}).get("value", "N/A")
        genre = row.get("genre", {}).get("value", "N/A")
        description = row.get("description", {}).get("value", "N/A")
        starring = row.get("starring", {}).get("value", "N/A")
        director = row.get("director", {}).get("value", "N/A")
        #image = row.get("image", {}).get("value", "N/A")
        
        film_clean = removePathPrefix(film)
        genre_clean = genre
        description_clean = removePathPrefix(description)
        starring_clean = removePathPrefix(starring)
        director_clean = removePathPrefix(director)
        image_clean = removePathPrefix(image)

        if image_clean == "N/A":
            image_clean = get_movie_data_omdb(film_clean, OMDB_API_KEY)["poster_url"] if get_movie_data_omdb(film_clean, OMDB_API_KEY) else "N/A"

        dico_genres_films.setdefault(genre_clean, []).append(film_clean)
        dico_films_descriptions.setdefault(film_clean, {"description": description_clean, "starring": [], "director": director_clean, "image": image_clean})
        dico_films_descriptions[film_clean]["starring"].append(starring_clean)
    
    return dico

def keepTopNResults(results, N):

    # Garder uniquement les 5 genres avec les plus de films
    sorted_genres = sorted(results["results"]["bindings"]["genres"].items(), key=lambda item: len(item[1]), reverse=True)
    topN_genres = dict(sorted_genres[:N])
    results["results"]["bindings"]["genres"] = topN_genres

    return results

def get_movie_data_omdb(movie_title, api_key):
    # L'URL de base d'OMDb
    url = "http://www.omdbapi.com/"

    url_poster = "http://img.omdbapi.com/"
    
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
            print(f"Erreur OMDb : {data.get('Error')}")
            return None
            
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        return None
