async function createPost() {
    const content = document.getElementById("post-content").value;
    if (!content) {
        alert("Le contenu de la publication ne peut pas être vide.");
        return;
    }
    try {
        const response = await fetch("/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: content })
        });
        if (response.ok) {
            alert("Publication créée avec succès !");
            document.getElementById("post-content").value = "";
            loadPosts();
        } else {
            alert("Erreur lors de la création de la publication.");
        }
    } catch (error) {
        console.error("Erreur de connexion :", error);
        alert("Erreur de connexion. Veuillez réessayer plus tard.");
    }
}

async function loadPosts() {
    const postsDiv = document.getElementById("posts");
    postsDiv.innerHTML = '<div class="loading-spinner"></div>'; // Affiche le spinner pendant le chargement

    try {
        const response = await fetch("/posts");
        if (response.ok) {
            const posts = await response.json();
            if (posts.length > 0) {
                postsDiv.innerHTML = posts.map(post => `
                    <div class="post">
                        <p>${post.content} <em>${new Date(post.created_at).toLocaleString()}</em></p>
                    </div>
                `).join("");
            } else {
                postsDiv.innerHTML = "<p>Aucune publication à afficher.</p>";
            }
        } else {
            postsDiv.innerHTML = "<p>Erreur lors du chargement des publications.</p>";
        }
    } catch (error) {
        console.error("Erreur de chargement des publications :", error);
        postsDiv.innerHTML = "<p>Erreur de connexion. Veuillez réessayer plus tard.</p>";
    }
}

document.addEventListener("DOMContentLoaded", loadPosts);
