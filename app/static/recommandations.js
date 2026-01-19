/**
 * Gestion des recommandations de films
 */

function getRecommendations(userProfil) {
    // const ok = checkMarked();

    // if (!ok) {
    //     alert("Merci de noter tous les films avant d’obtenir des recommandations.");
    //     return;
    // }

    console.log("Toutes les cartes sont notées. Recommandations à venir.");
    // Faire une requête POST au serveur Flask vers l'endpoint /recommendations
    fetch("/api/reco", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ profil: userProfil })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
}

function sendRatings() {
    // Construction du profil utilisateur 
    const cards = document.querySelectorAll(".film-card");
    const userProfil = {};
    cards.forEach(card => {
        const film = card.dataset.film;
        const activeBtn = card.querySelector(".btn.active");
        const rating = activeBtn ? activeBtn.dataset.rating : null;
        userProfil[film] = rating;
    });

    console.log("Profil utilisateur :", userProfil);
    getRecommendations(userProfil);
}


