$(document).ready(function() {
    // Simuler l'état de connexion (à remplacer par une vérification réelle)
    var isConnected = false; // Remplacer par la vérification réelle de connexion

    // Gérer l'affichage des boutons en fonction de l'état de connexion
    function updateUserButtons() {
        if (isConnected) {
            $("#signup-button, #login-button").hide();
            $("#logout-button").show();
        } else {
            $("#signup-button, #login-button").show();
            $("#logout-button").hide();
        }
    }

    // Initialiser les boutons
    updateUserButtons();

    // Retourner en haut de page lors du clic sur le logo et afficher la page d'accueil
    $("#logo").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        $(".page-section").hide();
        $("#home").show();
    });

    // Afficher la bulle d'information lors du survol
    $(".expandable").mouseenter(function() {
        var sectionId = $(this).data("section");
        var $infoBubble = $("#" + sectionId);
        $infoBubble.stop(true, true).fadeIn(500);
    }).mouseleave(function() {
        var sectionId = $(this).data("section");
        var $infoBubble = $("#" + sectionId);
        $infoBubble.stop(true, true).fadeOut(500);
    });

    // Gestion du clic sur les boutons
    $("#signup-button").click(function() {
        $('html, body').animate({
            scrollTop: $("#signup-section").offset().top
        }, 1000, function() {
            $("#signup-form").show();
            $("#login-form").hide();
            $("#signup-title").text("Inscrivez-vous maintenant !");
            $("#signup-button").addClass('active');
            $("#login-button").removeClass('active');
        });
    });

    $("#login-button").click(function() {
        $('html, body').animate({
            scrollTop: $("#signup-section").offset().top
        }, 1000, function() {
            $("#signup-form").hide();
            $("#login-form").show();
            $("#signup-title").text("Connecte-toi vite !");
            $("#signup-button").removeClass('active');
            $("#login-button").addClass('active');
        });
    });

    $("#logout-button").click(function() {
        isConnected = false; // Simuler la déconnexion
        updateUserButtons();
    });

    // Gestion de la navigation pour afficher et masquer les sections
    $(".nav-link").click(function(e) {
        e.preventDefault();
        var targetSection = $(this).attr('href').substring(1);
        $(".page-section").hide();  // Masquer toutes les sections
        $("#" + targetSection).show();  // Afficher la section cible
    });

    // Afficher la page d'accueil par défaut
    $("#home").show();

    // Charger les informations de l'utilisateur
    function loadUserProfile() {
        // Exemple de données utilisateur
        var user = {
            username: "John Doe",
            age: 25,
            region: "Île-de-France",
            profilePic: "{{ url_for('static', filename='images/profile-pic.jpg') }}",  // Remplacez par le chemin réel de l'image
            posts: [
                "Publication 1: Lorem ipsum dolor sit amet.",
                "Publication 2: Consectetur adipiscing elit.",
                "Publication 3: Integer nec odio. Praesent libero."
            ]
        };

        // Mettre à jour les informations de profil
        $("#username").text(user.username);
        $("#user-age-region").text(user.age + ", " + user.region);
        $("#profile-pic").attr("src", user.profilePic);

        // Charger les publications
        var postsContainer = $("#posts-container");
        user.posts.forEach(function(post) {
            var postElement = $("<div class='post'></div>").text(post);
            postsContainer.append(postElement);
        });
    }

    // Appeler la fonction pour charger le profil utilisateur lors de l'affichage de la page de profil
    $(".nav-link[href='#profile']").click(function() {
        loadUserProfile();
    });
});
