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

// Fonction pour obtenir le CSRF token depuis la meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Exemple de fonction pour le like d'une publication
async function likePost(postId) {
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
            // Mettre à jour l'interface utilisateur
            const result = await response.json();
            document.querySelector(`#post-${postId} .like-count`).textContent = result.likes;
        } else {
            console.error('Erreur lors du like de la publication');
        }
    } catch (error) {
        console.error('Erreur réseau :', error);
    }
}

function openAuthModal() {
    document.getElementById('auth-modal').style.display = 'block';
}

function closeAuthModal() {
    document.getElementById('auth-modal').style.display = 'none';
}

function showLoginForm() {
    document.getElementById('login-form').classList.add('active');
    document.getElementById('register-form').classList.remove('active');
}

function showRegisterForm() {
    document.getElementById('login-form').classList.remove('active');
    document.getElementById('register-form').classList.add('active');
}

function openAuthModal() {
    var modal = document.getElementById('auth-modal');
    modal.style.display = 'block';
}

function closeAuthModal() {
    var modal = document.getElementById('auth-modal');
    modal.style.display = 'none';
}
