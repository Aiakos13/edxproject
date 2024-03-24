function loadAvatar(upload_field, image_tag) {
    if (upload_field.files && upload_field.files[0] ) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.addEventListener("load", function() {
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");

                if (img.width >= img.height) {
                    canvas.width = img.height;
                    canvas.height = img.height;
                    ctx.drawImage(img, (img.width - img.height) / 2, 0, img.height, img.height, 0, 0, canvas.width, canvas.height);
                } else {
                    canvas.width = img.width;
                    canvas.height = img.width;
                    ctx.drawImage(img, 0, (img.height - img.width) / 2, img.width, img.width, 0, 0, canvas.width, canvas.height);
                }

                image_tag.src = canvas.toDataURL();
                uploadAvatar(image_tag.src);
            });
            img.src = e.target.result;
        };
        reader.readAsDataURL(upload_field.files[0]);
    }
}

function sendFollow(user_to_follow) {
    return new Promise(function(resolve, reject) {
        const request = new XMLHttpRequest();
        request.onload = function() {
            resolve(JSON.parse(this.responseText));
        };
        request.onerror = reject;
        request.open("POST", "/follow");

        const data = new FormData();
        data.append("user_to_follow", user_to_follow);
        request.send(data);
    });
}

function uploadAvatar(imageData) {
    return new Promise(function(resolve, reject) {
        const request = new XMLHttpRequest();
        request.onload = function() {};
        request.onerror = reject;
        request.open("POST", "/avatar");

        const data = new FormData();
        data.append("image", imageData);
        request.send(data);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // Change avatar link
    const avatar_btn = document.querySelector("#change-avatar-link");
    const image_tag = document.querySelector("#avatar-img");

    if (avatar_btn !== null) {
        const upload_field = document.querySelector("#upload-avatar");
        upload_field.onchange = (e) => {
            loadAvatar(upload_field, image_tag);
        };

        avatar_btn.onclick = (e) => {
            upload_field.click();
        };
    }

    // Set links
    document.querySelectorAll(".img-gallery").forEach((el) => {
        // Set onclick
        el.onclick = (e) => {
            window.location.href = "/post/" + e.target.dataset.postId;
        };

        // Set cursor to pointer
        el.onmouseover = (e) => {
            e.target.style.cursor = "pointer";
        };

        // Initialize tooltips
        $('[data-toggle="tooltip"]').tooltip();
    });

    // Follow
    const follow_btn = document.querySelector("button#follow-btn");
    if (follow_btn != null && !(follow_btn.disabled)) {
        follow_btn.onclick = (e) => {
            const user_to_follow = parseInt(window.location.pathname.split("/")[2]);
            sendFollow(user_to_follow)
                .then(function(result) {
                    // Update followers count
                    document.querySelector("#followers_count").innerText = result.followers;
                })
                .then(function(result) {
                    // Disable button
                    e.target.disabled = true;
                });
        };
    }
});
