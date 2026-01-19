from openai import OpenAI

# Initialize the client
client = OpenAI(
    base_url="https://ollama-ui.pagoda.liris.cnrs.fr/api",  
    api_key="sk-35729c1f15074008972ee602959d9f7b",         #   (go to profile - bottom left, account)
)

# Call the 70B model
response = client.chat.completions.create(
        model="llama3:70b",
        messages=[
            {"role": "system", "content": "Tu es un traducteur de requêtes plein texte vers SPARQL. Tu utilises un graphe qui contient uniquement ?film dbo:director ?director, ?film dbo:starring ?actor, ?film dbo:genre ?genre et ?film dbo:description ?description. Tu connais des éléments de modèle suivant : <http://dbpedia.org/resource/Comedy>. La requete doit repourner : ?film l'url du film, ?directors la liste des uri des realisateurs séparés par une virgule et un espace, ?genres la liste des uri des genres séparés par une virgule et un espace et ?actors liste des uri des acteurs séparés par une virgule et un espace. Tu ne dois répondre qu'en SPARQL, aucun texte, aucune explication en sus."},
            {"role": "user", "content": "les films réalisés par Blair Treu"}
        ],
        temperature=0.7
    )

print(response.choices[0].message.content)
