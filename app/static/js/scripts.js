
async function createPost() {
    const postContent = document.getElementById("post-content");
    if (postContent && postContent.value) {
        try {
            const response = await fetch("/posts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ content: postContent.value })
            });
            if (response.ok) {
                alert("Publication créée avec succès !");
                postContent.value = "";
                loadPosts();
            } else {
                alert("Erreur lors de la création de la publication.");
            }
        } catch (error) {
            console.error("Erreur de connexion :", error);
            alert("Erreur de connexion. Veuillez réessayer plus tard.");
        }
    } else {
        alert("Le contenu de la publication ne peut pas être vide.");
    }
}

async function loadPosts() {
    const postsDiv = document.getElementById("posts");
    if (postsDiv) {
        postsDiv.innerHTML = '<div class="loading-spinner"></div>';

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
}

function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

async function likePost(postId) {
    if (postId) {
        try {
            const response = await fetch(`/posts/${postId}/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({})
            });
            if (response.ok) {
                const result = await response.json();
                const likeCountElement = document.querySelector(`#post-${postId} .like-count`);
                if (likeCountElement) {
                    likeCountElement.textContent = result.likes;
                }
            } else {
                console.error('Erreur lors du like de la publication');
            }
        } catch (error) {
            console.error('Erreur réseau :', error);
        }
    }
}

function toggleVisibility(id) {
    const form = document.getElementById(id);
    if (form) {
        form.style.display = (form.style.display === "none" || !form.style.display) ? "block" : "none";
    }
}

// Ajustement dynamique des couleurs de texte
function adjustTextColors() {
    const textElements = document.querySelectorAll('.text-adapt');
    textElements.forEach(element => {
        const bgColor = window.getComputedStyle(element.parentElement).backgroundColor || window.getComputedStyle(element).backgroundColor;
        if (bgColor) {
            const rgb = bgColor.match(/\d+/g);
            if (rgb) {
                const brightness = Math.round(((parseInt(rgb[0]) * 299) +
                                               (parseInt(rgb[1]) * 587) +
                                               (parseInt(rgb[2]) * 114)) / 1000);
                element.style.color = (brightness > 125) ? '#1dff00' : '#e6e600';
                element.style.textShadow = (brightness > 125) ? '1px 1px 2px rgba(0, 0, 0, 0.5)' : '1px 1px 2px rgba(255, 255, 255, 0.5)';
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    adjustTextColors();
});
