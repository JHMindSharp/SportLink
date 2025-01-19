// app/static/js/profile_view.js

document.addEventListener("DOMContentLoaded", function() {
    const coverPhotoElem = document.querySelector('.cover-photo');
    if (coverPhotoElem) {
        const coverUrl = coverPhotoElem.getAttribute('data-cover-img');
        if (coverUrl) {
            coverPhotoElem.style.backgroundImage = `url('${coverUrl}')`;
        }
    }

    const profilePhotoElem = document.querySelector('.profile-photo');
    if (profilePhotoElem) {
        const profileUrl = profilePhotoElem.getAttribute('data-profile-img');
        if (profileUrl) {
            profilePhotoElem.style.backgroundImage = `url('${profileUrl}')`;
        }
    }
});
