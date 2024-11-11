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

// Fonctions pour gérer l'affichage des modales
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

// Fonctions pour afficher les formulaires de connexion et d'inscription
function showLogin() {
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('registerForm').classList.remove('active');
    document.querySelector('.tabs .tab:nth-child(1)').classList.add('active');
    document.querySelector('.tabs .tab:nth-child(2)').classList.remove('active');
}

function showRegister() {
    document.getElementById('registerForm').classList.add('active');
    document.getElementById('loginForm').classList.remove('active');
    document.querySelector('.tabs .tab:nth-child(2)').classList.add('active');
    document.querySelector('.tabs .tab:nth-child(1)').classList.remove('active');
}

// Fonction pour fermer la modale
function closeModal() {
    document.querySelector('.modal').style.display = 'none';
}

// Améliorations des fonctions modales
function openAuthModal() {
    var modal = document.getElementById('auth-modal');
    modal.style.display = 'block';
}

function closeAuthModal() {
    var modal = document.getElementById('auth-modal');
    modal.style.display = 'none';
}

// Script pour ajuster dynamiquement la couleur du texte
document.addEventListener("DOMContentLoaded", function() {
    const profileHeader = document.querySelector('.profile-header');
    const userName = document.querySelector('.user-info h1');

    if (profileHeader && userName) {
        const bgColor = window.getComputedStyle(profileHeader).backgroundColor;
        const rgb = bgColor.match(/\d+/g);

        if (rgb) {
            const brightness = Math.round(((parseInt(rgb[0]) * 299) +
                                           (parseInt(rgb[1]) * 587) +
                                           (parseInt(rgb[2]) * 114)) / 1000);

            userName.style.color = (brightness > 125) ? '#000' : '#fff'; // Noir si clair, blanc si foncé
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const profilePhoto = document.querySelector('.profile-photo');
    const coverPhoto = document.querySelector('.cover-photo');

    function enableZoom(element) {
        let scale = 1;
        let posX = 0;
        let posY = 0;

        element.addEventListener('wheel', (e) => {
            e.preventDefault();
            scale += e.deltaY * -0.01;
            scale = Math.min(Math.max(.5, scale), 3);
            element.style.transform = `scale(${scale})`;
        });

        let isDragging = false;
        let startX, startY;

        element.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - posX;
            startY = e.clientY - posY;
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                posX = e.clientX - startX;
                posY = e.clientY - startY;
                element.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
            }
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    }

    enableZoom(profilePhoto);
    enableZoom(coverPhoto);
});
