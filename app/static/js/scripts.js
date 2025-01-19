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
    const textElements = document.querySelectorAll('.text-adapt');

    textElements.forEach(element => {
        // Obtenir la couleur d'arrière-plan de l'élément parent ou de l'élément lui-même
        let bgColor = window.getComputedStyle(element.parentElement).backgroundColor || window.getComputedStyle(element).backgroundColor;
        console.log(`Couleur d'arrière-plan pour l'élément: ${bgColor}`); // Journal de débogage

        let rgb = bgColor.match(/\d+/g);

        if (rgb) {
            // Calcul de la luminosité
            const brightness = Math.round(((parseInt(rgb[0]) * 299) +
                                           (parseInt(rgb[1]) * 587) +
                                           (parseInt(rgb[2]) * 114)) / 1000);
            console.log(`Luminosité calculée: ${brightness}`); // Journal de débogage

            // Adapter la couleur du texte en fonction de la luminosité et ajouter un contour
            element.style.color = (brightness > 125) ? '#1dff00' : '#e6e600'; // Vert clair si fond clair, jaune si fond foncé
            element.style.textShadow = (brightness > 125) ? '1px 1px 2px rgba(0, 0, 0, 0.5)' : '1px 1px 2px rgba(255, 255, 255, 0.5)'; // Contour sombre ou clair pour améliorer la lisibilité
            console.log(`Couleur de texte appliquée: ${element.style.color}`); // Journal de débogage
        } else {
            console.log(`Impossible de déterminer la couleur d'arrière-plan pour l'élément.`);
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const textElements = document.querySelectorAll('.text-adapt');

    textElements.forEach((element, index) => {
        // Calculer la couleur dégradée basée sur la position de l'élément
        const percentage = index / (textElements.length - 1);
        const red = Math.round(255 * (1 - percentage));
        const green = Math.round(255 * percentage);
        const color = `rgb(${red}, ${green}, 0)`;

        element.style.color = color;
    });
});

function toggleVisibility(id) {
    const form = document.getElementById(id);
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const coverPhoto = document.querySelector('.cover-photo');
    const userName = document.getElementById('user-name');

    // Create an off-screen canvas to analyze the cover image
    const img = new Image();
    img.src = coverPhoto.style.backgroundImage.slice(5, -2);
    img.crossOrigin = 'Anonymous';

    img.onload = function() {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        // Get pixel data at the center of the image
        const x = canvas.width / 2;
        const y = canvas.height / 2;
        const pixel = ctx.getImageData(x, y, 1, 1).data;

        // Calculate brightness
        const brightness = (pixel[0] * 299 + pixel[1] * 587 + pixel[2] * 114) / 1000;

        // Set text color based on brightness
        userName.style.color = (brightness > 125) ? 'black' : '#00FF00';
    };
});

// Gestion des messages flash
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll('.flash-messages .alert');

    // Supprimer automatiquement les messages après 5 secondes
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (message.parentElement) {
                    message.parentElement.removeChild(message);
                }
            }, 500); // Attendre la fin de la transition avant de supprimer l'élément
        }, 5000); // 5 secondes avant de commencer à disparaître

        // Permettre la fermeture au clic
        message.addEventListener('click', () => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (message.parentElement) {
                    message.parentElement.removeChild(message);
                }
            }, 500);
        });

        // Faire disparaître au survol
        message.addEventListener('mouseenter', () => {
            message.style.opacity = '0.6';
        });

        message.addEventListener('mouseleave', () => {
            message.style.opacity = '1';
        });
    });
});
