async function createPost() {
    const content = document.getElementById("post-content").value;
    const response = await fetch("/posts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_id: 1, content: content }) // Remplacez 1 par l'ID utilisateur dynamique
    });
    if (response.ok) {
        alert("Post created successfully!");
        document.getElementById("post-content").value = "";
        loadPosts();
    }
}

async function loadPosts() {
    const response = await fetch("/posts");
    const posts = await response.json();
    const postsDiv = document.getElementById("posts");
    postsDiv.innerHTML = posts.map(post => `<p>${post.content} <em>${post.created_at}</em></p>`).join("");
}

document.addEventListener("DOMContentLoaded", loadPosts);
