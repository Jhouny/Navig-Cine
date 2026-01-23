
document.querySelectorAll('.film-card').forEach(card => {
    const origtitle = card.querySelector('h3').textContent;
    // Remove parenthetical info from title for better search
    const title = origtitle.replace(/\s*\(.*?\)\s*/g, '');

    const img = card.querySelector('img');
    // Essayer de récupérer l'image depuis OMDb
    fetch(`/api/poster?title=${encodeURIComponent(title)}`).then(response => {
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

});