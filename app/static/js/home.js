// app/static/js/home.js

document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card3D');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // On toggle une classe .flipped
            card.querySelector('.card3D-inner').classList.toggle('flipped');
        });
    });
});
