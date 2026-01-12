/**
 * Gestion des recommandations de films
 */

async function sendRatings(ratings) {
    try {
        const response = await fetch("/calculate_recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(ratings)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erreur lors du calcul des recommandations:", error);
        throw error;
    }
}