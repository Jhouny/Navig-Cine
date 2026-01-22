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

    console.log("Categories and its films:",filmsByCategory);
    console.log("Films and its infos:",filmsInfos);

    const filmList = document.querySelector(".film-list");
    filmList.innerHTML = "";
    
    const categories = Object.keys(filmsByCategory)
        .sort(() => Math.random() - 0.5)
        .slice(0, 5);

    categories.forEach(category => {
        const films = [];

        while (films.length < 2) {
            const film = getUnusedFilmFromCategory(category);
            if (!film){
                // plus rien de dispo
                notAvailabe = true;
                break;
            }; 
            films.push(film);
        }

        // Créer la section pour chacune des catégories
        const row = document.createElement("section");
        row.classList.add("film-row");

        // on prend 2 films par ligne pour l'affichage


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
            
            // Essayer de récupérer l'image depuis OMDb
            fetch(`/api/poster?title=${encodeURIComponent(filmTitle)}`).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Erreur lors de la récupération de l'affiche.");
                }
            }).then(data => {
                // Make a HEAD request to check if the image exists
                fetch(data, { method: 'HEAD' })
                    .then(headResponse => {
                        if (headResponse.ok) {
                            img.src = data;
                        } else {
                            // Image par défaut si l'URL n'est pas valide
                            img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
                        }
                    }
                ).catch(() => {
                    // Image par défaut en cas d'erreur
                    img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
                });
            }).catch(error => {
                console.error("Erreur lors de la récupération de l'affiche :", error);
                // Image par défaut si échec
                img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
            });

            // Si pas d'image dispo, mettre une image aléatoire
            if (!img.src || img.src === "N/A")
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
                <button class="btn skip">⏭ Didn't watch</button>
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
    initializeFilmCards();

}

function getUnusedFilmFromCategory(category) {
    const films = filmsByCategory[category] || [];

    const available = films.filter(
        film => !isFilmAlreadyAdded(film)
    );

    if (available.length === 0) return null;

    const idx = Math.floor(Math.random() * available.length);
    return available[idx];
}

function isFilmAlreadyAdded(filmTitle) {
    return [...document.querySelectorAll(".film-card")]
        .some(card => card.dataset.film === filmTitle);
}

async function initializeFilmCards() {
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
    const filmTitle = list[randomIndex];
    const img = card.querySelector(".poster");
    // Essayer de récupérer l'image depuis OMDb
    fetch(`/api/poster?title=${encodeURIComponent(filmTitle)}`)
    .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
            throw new Error(
              "Erreur lors de la récupération de l'affiche.",
            );
        }
    })
    .then((data) => {
    // Make a HEAD request to check if the image exists
    fetch(data, { method: "HEAD" })
        .then((headResponse) => {
            if (headResponse.ok) {
                img.src = data;
            } else {
                // Image par défaut si l'URL n'est pas valide
                img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
            }
        })
        .catch(() => {
            // Image par défaut en cas d'erreur
            img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
        });
    })
    .catch((error) => {
        console.error(
            "Erreur lors de la récupération de l'affiche :",
            error,
        );
        // Image par défaut si échec
        img.src = `https://picsum.photos/800/400?random=${Math.random()}`;
    });

    // Si pas d'image dispo, mettre une image aléatoire
    if (!img.src || img.src === "N/A")
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

        if (!activeBtn) return;

        let score = 0;
        if (activeBtn.classList.contains("like")) score = 1;
        else if (activeBtn.classList.contains("dislike")) score = -1;
        else if (activeBtn.classList.contains("skip")) score = 0;

        userProfil.Films[film] = score;

        const meta = filmsInfos[film];
        if (!meta) return;

        Object.entries(filmsByCategory).forEach(([genre, films]) => {
            if (films.includes(film)) {
                userProfil.genres[genre] = (userProfil.genres[genre] || 0) + score;
            }
        });

        normalizeToArray(meta.director).forEach(director => {
            console.log("Director:", director);
            userProfil.realisateurs[director] =
                (userProfil.realisateurs[director] || 0) + score;
        });
        
        normalizeToArray(meta.starring).forEach(actor => {
            userProfil.acteurs[actor] =
                (userProfil.acteurs[actor] || 0) + score;
        });

    });

    const uid = Math.random().toString(16).slice(2);

    console.log("Profil utilisateur :", userProfil);

    getRecommendations(userProfil, uid);

    //window.location.href = `/recommendations?uid=` + encodeURIComponent(uid);
}

function isValidValue(v) {
    return v && v !== "N/A";
}

function normalizeToArray(value) {
    if (!isValidValue(value)) return [];
    if (Array.isArray(value)) {
        return value.filter(v => isValidValue(v));
    }
    return [value];
}