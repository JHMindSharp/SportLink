$(document).ready(function() {
    // Retourner en haut de page lors du clic sur le logo
    $("#logo").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
    });

    // Sections déroulantes
    $("section > h2").click(function() {
        $(this).toggleClass("active");
        $(this).next("div").slideToggle();
    });
});
