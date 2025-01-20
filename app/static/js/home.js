document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card3D');
    if (cards.length > 0) {
        cards.forEach(card => {
            const cardInner = card.querySelector('.card3D-inner');
            if (cardInner) {
                card.addEventListener('click', () => {
                    cardInner.classList.toggle('flipped');
                });
            }
        });
    }
});
