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
        image = row.get("image", {}).get("value", "N/A")
        
        film_clean = removePathPrefix(film)
        genre_clean = removePathPrefix(genre)
        description_clean = removePathPrefix(description)
        starring_clean = removePathPrefix(starring)
        director_clean = removePathPrefix(director)
        image_clean = removePathPrefix(image)

        dico_genres_films.setdefault(genre_clean, []).append(film_clean)
        dico_films_descriptions.setdefault(film_clean, {"description": description_clean, "starring": [], "director": director_clean, "image": image_clean})
        dico_films_descriptions[film_clean]["starring"].append(starring_clean)
    
    return dico

def keepTopNResults(results, N):

    # Garder uniquement les 5 genres avec les plus de films
    sorted_genres = sorted(results["results"]["bindings"].items(), key=lambda item: len(item[1]), reverse=True)
    topN_genres = dict(sorted_genres[:N])
    results["results"]["bindings"] = topN_genres

    return results

