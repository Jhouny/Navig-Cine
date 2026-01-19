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
        
        film_clean = removePathPrefix(film)
        genre_clean = removePathPrefix(genre)
        description_clean = removePathPrefix(description)

        dico_genres_films.setdefault(genre_clean, []).append(film_clean)
        dico_films_descriptions[film_clean] = description_clean

    return dico
