document.addEventListener('DOMContentLoaded', () => {
  const whatsNewBubble = document.getElementById('whatsNewBubble');
  const placeholderText = document.getElementById('placeholder-text');
  const createPostForm = document.getElementById('createPostForm');
  const cancelPostBtn = document.getElementById('cancelPostBtn');

  if (whatsNewBubble && placeholderText && createPostForm) {
      whatsNewBubble.addEventListener('click', () => {
          if (!createPostForm.style.display || createPostForm.style.display === 'none') {
              createPostForm.style.display = 'block';
              placeholderText.style.display = 'none';
          }
      });
  }

  if (cancelPostBtn) {
      cancelPostBtn.addEventListener('click', (e) => {
          e.preventDefault();
          if (createPostForm && placeholderText) {
              createPostForm.style.display = 'none';
              placeholderText.style.display = 'block';
          }
      });
  }
});
