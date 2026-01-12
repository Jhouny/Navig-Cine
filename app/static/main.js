/**
 * Point d'entrée principal de l'application
 */

async function init() {
    console.log("Initialisation de l'application...");

    // Test de la connexion au serveur SPARQL
    try {
        const test = await executeSparql();
        console.log("Connexion SPARQL réussie. Genres récupérés:", test);
    } catch (error) {
        console.error("Erreur de connexion au serveur SPARQL:", error);
    }

    // // Initialiser les cartes de films
    // initializeFilmCards();

    // // Charger les genres depuis SPARQL
    // const genres = await fetchGenresFromSPARQL();
    // genres.forEach(result => {
    //     const genre = result.genre.value;
    //     const count = result.count.value;
    //     console.log(`Genre: ${genre}, Films: ${count}`);
    // });

    // // Configurer le bouton de soumission
    // const submitBtn = document.getElementById('submit-ratings');
    // if (submitBtn) {
    //     submitBtn.addEventListener('click', async () => {
    //         try {
    //             const ratings = getRatings();
    //             const data = await sendRatings(ratings);
    //             alert("Recommandations calculées !");
    //             console.log(data);
    //         } catch (error) {
    //             alert("Erreur lors du calcul des recommandations.");
    //         }
    //     });
    // }
}

// Lancer l'application au chargement de la page
document.addEventListener('DOMContentLoaded', init);