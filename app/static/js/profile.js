document.addEventListener("DOMContentLoaded", () => {
    const likeButtons = document.querySelectorAll(".like-btn");
    const dislikeButtons = document.querySelectorAll(".dislike-btn");

    likeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            console.log("Liked post ID:", button.dataset.postId);
            // Ajouter la logique pour le bouton J'aime
        });
    });

    dislikeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            console.log("Disliked post ID:", button.dataset.postId);
            // Ajouter la logique pour le bouton Je n'aime pas
        });
    });
});
