// app/static/js/profile_view.js

document.addEventListener('DOMContentLoaded', () => {
    const whatsNewBubble = document.getElementById('whatsNewBubble');
    const placeholderText = document.getElementById('placeholder-text');
    const createPostForm = document.getElementById('createPostForm');
    const cancelPostBtn = document.getElementById('cancelPostBtn');
  
    // Au clic sur la bulle "Quoi de neuf"
    if (whatsNewBubble && placeholderText && createPostForm) {
      whatsNewBubble.addEventListener('click', () => {
        if (!createPostForm.style.display || createPostForm.style.display === 'none') {
          createPostForm.style.display = 'block';
          placeholderText.style.display = 'none';
        }
      });
    }
  
    // Bouton annuler
    if (cancelPostBtn) {
      cancelPostBtn.addEventListener('click', (e) => {
        e.preventDefault();
        createPostForm.style.display = 'none';
        placeholderText.style.display = 'block';
      });
    }
  });
  