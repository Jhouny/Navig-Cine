const ratings = {};

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