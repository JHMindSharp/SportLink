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

    // Retourner en haut de page lors du clic sur le logo
    $("#logo").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
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
});
