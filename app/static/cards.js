/**
 * Gestion de l'interface des cartes de films
 */

ratings = {};

filmsByCategory = {

};

filmsInfos = {
};

// Les films seront récupérés dans le serveur GraphDB

async function createFilmCards() {
    const dicos = await fetchFilmsAndGenre();
    console.log("Genres fetched from SPARQL:", dicos);
    filmsByCategory = dicos["genres"];
    filmsInfos = dicos["films"];

    console.log(filmsByCategory);
    console.log(filmsInfos);

    const filmList = document.querySelector(".film-list");
    filmList.innerHTML = "";
    
    // Choisir 5 catégories aléatoires
    const categories = Object.keys(filmsByCategory)
        .sort(() => Math.random() - 0.5)
        .slice(0, 5);

    categories.forEach(category => {
        
        // Créer la section pour chacune des catégories
        const row = document.createElement("section");
        row.classList.add("film-row");

        // on prend 2 films par ligne pour l'affichage
        const films = filmsByCategory[category].slice(0, 2);

        films.forEach(filmTitle => {

            // Créer la carte de chacun de film et y mettre les bonnes infos
            const card = document.createElement("div");
            card.classList.add("film-card");
            card.dataset.film = filmTitle;
            card.dataset.category = category;
            card.dataset.director = filmsInfos[filmTitle]["director"];
            card.dataset.actors = filmsInfos[filmTitle]["actors"];

            const img = document.createElement("img");
            img.classList.add("poster");
            img.src = `https://picsum.photos/800/400?random=${Math.random()}`;

            // Affichage de la carte
            const info = document.createElement("div");
            info.classList.add("film-info");

            const h3 = document.createElement("h3");
            h3.textContent = filmTitle;

            const p = document.createElement("p");
            p.textContent = filmsInfos[filmTitle]["description"] || "Description indisponible.";

            // Boutons (like, dislike)
            const actions = document.createElement("div");
            actions.classList.add("actions");

            actions.innerHTML = `
                <button class="btn like">👍 Like</button>
                <button class="btn dislike">👎 Dislike</button>
                <button class="btn skip">⏭ Didn’t watch</button>
            `;

            info.appendChild(h3);
            info.appendChild(p);
            info.appendChild(actions);

            card.appendChild(img);
            card.appendChild(info);

            row.appendChild(card);
        });

        filmList.appendChild(row);
    });

}

function initializeFilmCards() {
    console.log("film cards:", document.querySelectorAll(".film-card").length);

    document.querySelectorAll(".film-card").forEach(card => {
        const film = card.dataset.film;

        // Ajouter le bouton reload
        const reloadBtn = document.createElement('button');
        reloadBtn.textContent = "🔄";
        reloadBtn.classList.add('reload-btn');
        reloadBtn.style.position = "absolute";
        reloadBtn.style.top = "10px";
        reloadBtn.style.right = "10px";
        reloadBtn.style.zIndex = "10";

        reloadBtn.addEventListener('click', () => {
            const category = card.dataset.category;
            const newFilm = getRandomFilm(category, card);
            if (newFilm) {
                card.querySelector('h3').textContent = newFilm;
            }
        });
        card.style.position = "relative";
        card.appendChild(reloadBtn);

        // Ajouter des listeners aux boutons d'action
        const actionButtons = card.querySelectorAll(".btn");
        

        actionButtons.forEach(btn => {
            btn.addEventListener("click", () => {

                // Désactiver les autres boutons de la même carte
                actionButtons.forEach(b => b.classList.remove("active"));

                // Activer celui-ci
                btn.classList.add("active");

            });
        });

    });
}

function getRandomFilm(category, card) {
    const list = filmsByCategory[category] || [];
    if (list.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * list.length);
    const img = card.querySelector(".poster");
    img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
    return list[randomIndex];
}

function checkMarked() {
    const cards = document.querySelectorAll(".film-card");
    let allValid = true;

    cards.forEach(card => {
        const activeBtn = card.querySelector(".btn.active");
        if (!activeBtn) {
            allValid = false;
            card.style.outline = "2px solid #e04f5f";
        } else {
            card.style.outline = "none";
        }
    });

    return allValid;
}

function getRecommendations(userProfil, uid) {
    // Faire une requête POST au serveur Flask vers l'endpoint /recommendations
    fetch("/api/reco", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ profil: userProfil, uid: uid })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
}

function sendRatings() {
    const ok = checkMarked();
    if (!ok) {
        alert("Veuillez évaluer tous les films avant de continuer.");
        return;
    }
    
    // Construction du profil utilisateur 
    const cards = document.querySelectorAll(".film-card");
    const userProfil = {
        'Films' : {},
        'genres' : {},
        'realisateurs' : {},
        'acteurs' : {}
    };
    cards.forEach(card => {
        const film = card.dataset.film;
        const activeBtn = card.querySelector(".btn.active");
        const rating = activeBtn ? activeBtn.dataset.rating : null;
        userProfil['Films'][film] = rating;
    });

    const uid = Math.random().toString(16).slice(2);

    console.log("Profil utilisateur :", userProfil);
    getRecommendations(userProfil, uid);
    // Rediriger vers la page des recommandations
    window.location.href = `/recommendations?uid=` + encodeURIComponent(uid);
}
