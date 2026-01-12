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
    document.querySelectorAll(".film-card").forEach(card => {
        const film = card.dataset.film;
        const container = card.querySelector(".hearts");
        ratings[film] = 0;

        // Ajouter les cœurs
        for (let i = 1; i <= 5; i++) {
            const heart = document.createElement("span");
            heart.innerHTML = "♥";
            heart.classList.add("heart");

            heart.addEventListener("click", () => {
                ratings[film] = i;
                updateHearts(container, i);
            });

            container.appendChild(heart);
        }

        // Ajouter le bouton reload
        const reloadBtn = document.createElement('button');
        reloadBtn.textContent = "🔄";
        reloadBtn.classList.add('reload-btn');
        reloadBtn.style.position = "absolute";
        reloadBtn.style.top = "10px";
        reloadBtn.style.right = "10px";

        reloadBtn.addEventListener('click', () => {
            const category = card.dataset.category;
            const newFilm = getRandomFilm(category);
            if (newFilm) {
                card.querySelector('h3').textContent = newFilm;
            }
        });

        card.style.position = "relative";
        card.appendChild(reloadBtn);
    });
}

function updateHearts(container, count) {
    [...container.children].forEach((heart, index) => {
        heart.classList.toggle("filled", index < count);
    });
}

function getRandomFilm(category) {
    const list = filmsByCategory[category] || [];
    if (list.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * list.length);
    return list[randomIndex];
}

function getRatings() {
    return ratings;
}