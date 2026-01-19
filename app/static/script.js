const ratings = {};

const filmsByCategory = {
    "science-fiction": ["Inception", "Interstellar", "Blade Runner", "Matrix", "Ex Machina"],
    "romance": ["Amélie", "Titanic", "La La Land", "Pride & Prejudice", "Her"],
    "action": ["Mad Max", "John Wick", "Die Hard", "Gladiator", "The Dark Knight"],
    "comedy": ["Superbad", "The Hangover", "Monty Python", "Step Brothers", "Bridesmaids"],
    "horror": ["Get Out", "It", "The Shining", "A Quiet Place", "Hereditary"],
    "drama": ["The Godfather", "Forrest Gump", "Schindler's List", "Fight Club", "The Shawshank Redemption"]
};  

// Add hearts and reload button with their event listeners
document.querySelectorAll(".film-card").forEach(card => {
    const film = card.dataset.film;
    const container = card.querySelector(".hearts");
    ratings[film] = 0;

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

    const reloadBtn = document.createElement('button');
    reloadBtn.textContent = "🔄";
    reloadBtn.classList.add('reload-btn');
    reloadBtn.style.position = "absolute";
    reloadBtn.style.top = "10px";
    reloadBtn.style.right = "10px";

    reloadBtn.addEventListener('click', () => {
        const category = card.dataset.category; // Assure-toi que chaque card a un data-category
        const newFilm = get_film(category);
        if(newFilm) {
            card.querySelector('h3').textContent = newFilm;
        }
    });

    card.style.position = "relative"; // pour que le bouton s'affiche à droite du card
    card.appendChild(reloadBtn);

});

function updateHearts(container, count) {
    [...container.children].forEach((heart, index) => {
        heart.classList.toggle("filled", index < count);
    });
}

function sendRatings() {
    fetch("/calculate_recommendations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(ratings)
    })
    .then(res => res.json())
    .then(data => {
        alert("Recommandations calculées !");
        console.log(data);
    })
    .catch(err => {
        console.error(err);
        alert("Erreur lors du calcul des recommandations.");
    });
}

function list_films(category) {
    return filmsByCategory[category] || [];
}

function get_film(category) {
    const list = list_films(category);
    if(list.length === 0) return null; // sanity check

    const randomIndex = Math.floor(Math.random() * list.length);
    // on envoie un nouveau film aléatoire  
    return list[randomIndex];

}
