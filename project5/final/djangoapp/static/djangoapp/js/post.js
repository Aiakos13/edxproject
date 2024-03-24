function getDateTimeFormatted(dt_string) {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const dt = new Date(dt_string);

    const month = months[dt.getMonth()];
    const day = dt.getDate();
    const year = dt.getFullYear();
    let hour = dt.getHours();
    const mins = dt.getMinutes();
    let ampm = "a.m.";
    if (hour > 12) {
        hour -= 12;
        ampm = "p.m.";
    }

    return `${month} ${day}, ${year}, ${hour}:${mins} ${ampm}`;
}

function renewComments(comments) {
    const list = document.querySelector("#comments-list");
    list.innerHTML = "";
    comments.forEach((comment) => {
        // Whole block
        entity = document.createElement("div");
        entity.classList.add("comment-entity");

        // Info block
        info = document.createElement("div");
        info.classList.add("comment-info");
        info.classList.add("text-right");
        span1 = document.createElement("span");
        span1.classList.add("comment-author");
        span1.innerHTML = `<a href="/user/${comment.author_id}">` + comment.author_name + " </a>"
        span2 = document.createElement("span");
        span2.classList.add("comment-created");
        span2.innerText = comment.created;
        info.appendChild(span1);
        info.appendChild(span2);

        // Comment block
        comment_tag = document.createElement("div");
        comment_tag.classList.add("comment-text");
        comment_tag.innerText = comment.text;

        // Whole block
        entity.appendChild(info);
        entity.appendChild(comment_tag);

        list.appendChild(entity);
    });
}

function sendComment(postId) {
    return new Promise(function(resolve, reject) {
        const request = new XMLHttpRequest();
        request.onload = function() {
            resolve(JSON.parse(this.responseText));
        };
        request.onerror = reject;
        request.open("POST", "/comment");

        const data = new FormData(document.querySelector("#comment-form"));
        data.append("post_id", postId);
        request.send(data);
    });
}

function sendLike(postId) {
    return new Promise(function(resolve, reject) {
        const request = new XMLHttpRequest();
        request.onload = function() {
            resolve(JSON.parse(this.responseText));
        };
        request.onerror = reject;
        request.open("POST", "/like");

        const data = new FormData();
        data.append("post_id", postId);
        request.send(data);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // On new comment submit
    document.querySelector("#comment-form").onsubmit = (e) => {
        const postId = parseInt(window.location.pathname.split("/")[2]);
        sendComment(postId)
            .then(function(result) {
                // Renew comments list
                renewComments(result.comments);
            })
            .then(function(result) {
                // Renew comments count
                let count = parseInt(document.querySelector("#comments-count").innerText);
                count += 1;
                document.querySelector("#comments-count").innerText = count;
            });

        document.querySelector("#comment-input").value = "";
        return false;
    };

    // Like
    document.querySelector("button.like-btn").onclick = (e) => {
        const postId = parseInt(window.location.pathname.split("/")[2]);
        sendLike(postId)
            .then(function(result) {
                // Renew likes count
                document.querySelector("#likes-count").innerText = result.liked;
            })
            .then(function(result) {
                // Disable "Like" button
                e.target.disabled = true;
            });
    };
});
