document.addEventListener("DOMContentLoaded", () => {
    // On search submit
    document.querySelector("#search-form").onsubmit = () => {
        const query = document.querySelector("#search-query").value;
        if (!query) {
            return false;
        }
    };
});
