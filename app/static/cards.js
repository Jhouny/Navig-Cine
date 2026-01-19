/**
 * Gestion de l'interface des cartes de films
 */

const ratings = {};

const filmsByCategory = {
    "science-fiction": ["Inception", "Interstellar", "Blade Runner", "Matrix", "Ex Machina"],
    "romance": ["Amélie", "Titanic", "La La Land", "Pride & Prejudice", "Her"],
    "action": ["Mad Max", "John Wick", "Die Hard", "Gladiator", "The Dark Knight"],
    "comedy": ["Superbad", "The Hangover", "Monty Python", "Step Brothers", "Bridesmaids"],
    "horror": ["Get Out", "It", "The Shining", "A Quiet Place", "Hereditary"]
};

// Les films seront récupérés dans le serveur GraphDB
// const filmsByCategoryGraphDB = fetchFilmsByGenre();

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