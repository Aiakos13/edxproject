function applyFilters(filters) {
    const canvas = document.querySelector("canvas#new-photo");
    Caman(canvas, function () {
        this.revert(false);
        if (filters) {
            for (let filterName in filters) {
                if (filters.hasOwnProperty(filterName)) {
                    this[filterName](filters[filterName]);
                }
            };
        }
        this.render();
    });
}

function loadPhoto(fileInput, filters){
    if (fileInput.files && fileInput.files[0] ) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.addEventListener("load", function() {
                let image_tag = document.querySelector("img#new-photo");
                let canvas_tag = document.querySelector("canvas#new-photo");
                if (image_tag == null) {
                    document.querySelector("#image-placeholder").innerHTML = "";

                    image_tag_string = '<img id="new-photo" src="' + img.src + '" alt="">';
                    document.querySelector("#image-placeholder").innerHTML = image_tag_string;

                    image_tag = document.querySelector("img#new-photo");
                } else if (canvas_tag == null) {
                    image_tag.src = img.src;
                }
                Caman(image_tag, function() {
                    this.render(function() {
                        document.querySelector("canvas#new-photo").onclick = () => {
                            fileInput.click();
                        };

                        document.querySelector("#reset-filters-btn").click();
                    });
                });
            });
            img.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}

function uploadPhoto(imageData, description) {
    return new Promise(function(resolve, reject) {
        const request = new XMLHttpRequest();
        request.onload = function() {
            window.location.href = "/upload";
        };
        request.onerror = reject;
        request.open("POST", "upload");

        const data = new FormData();
        data.append("image", imageData);
        data.append("description", description);
        request.send(data);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    let filters = {};

    const fileInput = document.querySelector("#upload-photo");

    document.querySelector("img#new-photo").onclick = () => {
        fileInput.click();
    };
    fileInput.onchange = () => {
        loadPhoto(fileInput, filters);
    };

    // Set filters onclick events
    document.querySelectorAll(".filter-input").forEach((el) => {
        el.onchange = (e) => {
            const name = e.target.dataset.filter;
            const value = e.target.value;
            document.querySelector(`[data-filter-value='${name}']`).innerText = value;
            filters[name] = value;
            applyFilters(filters);
        };
    });

    // Reset Filters
    document.querySelector("#reset-filters-btn").onclick = (e) => {
        document.querySelectorAll(".filter-input").forEach((el) => {
            // Reset values
            const name = el.dataset.filter;
            let value;
            if (name == "gamma") {
                value = 1;
            } else {
                value = 0;
            }
            el.value = value;
            document.querySelector(`[data-filter-value='${name}']`).innerText = value;

            // Reset filters
            filters = {};
            applyFilters(filters);

            // Reset description
            document.querySelector("textarea").value = "";
        });
    };

    document.querySelector("#upload-photo-btn").onclick = (e) => {
        const canvas = document.querySelector("canvas#new-photo");
        
        const dataURL = canvas.toDataURL();
        const description = document.querySelector("textarea").value;
        uploadPhoto(dataURL, description);
    };
});
