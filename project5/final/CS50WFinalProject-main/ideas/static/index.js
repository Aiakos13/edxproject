const mainDiv = document.querySelector("#ideas");
const addbtn = document.querySelector("#btnforadd");

const getIdeas = async () => {
  const res = await fetch("allideas");
  const data = await res.json();
  return data;
};

document.addEventListener("DOMContentLoaded", async () => {
  let data = await getIdeas();
  data.forEach((i) => {
    let div = document.createElement("div");
    div.className = "col-lg-4 col-md-6 col-sm-12";
    div.innerHTML = `
    <div class="idea-card mb-3">
    <div class="card-body" id="id${i.pk}">
    <h5 class="card-title">${i.fields.title}</h5>
    <p class="card-text">${i.fields.description}</p>
    <p class="card-created card-link">${i.fields.created_at.slice(0, 10)}</p>
      <p class="card-user card-link">${i.fields.user}</p>
      </div>
      </div>`;
    mainDiv.appendChild(div);
  });
  data.forEach((j) => {
    let username = localStorage.getItem("username");
    if (j.fields.user == username) {
      let editbutton = document.createElement("button");
      let deletebutton = document.createElement("button");
      deletebutton.className = "deletebutton";
      deletebutton.innerHTML = "X";
      editbutton.className = "editbutton";
      editbutton.innerHTML = "✏️";
      let ideaid = document.querySelector(`#id${j.pk} h5`);
      deletebutton.className += ` ${j.pk}`;
      editbutton.className += ` ${j.pk}`;
      ideaid.appendChild(editbutton);
      ideaid.appendChild(deletebutton);
      deletebutton.addEventListener("click", (e) => {
        deleteIdea(e.target.classList[1]);
      });
      editbutton.addEventListener("click", (e) => {
        editIdea(e.target.classList[1]);
      });
    }
  });
});

addbtn.addEventListener("click", () => {
  let formdiv = document.querySelector(".addform");
  formdiv.style.display = "flex";
  let form = document.querySelector("#addideaform");
  let hidediv = document.querySelector(".hidediv");
  let username = localStorage.getItem("username");
  form.style.display = "flex";
  hidediv.innerHTML = `<div id="formdiv"
    <div class="mb-3">
    <label for="ideatitle" class="form-label">Idea Title</label>
    <input type="text" name="title" class="form-control" id="ideatitle" aria-describedby="emailHelp">
    </div>
    <div class="mb-3">
    <label for="ideadesc" class="form-label">Idea Description</label>
    <textarea type="text" name="description" class="form-control" id="ideadesc"></textarea>
    </div>
    <div class="mb-3">
    <label for="username" class="form-label">Username</label>
    <input value="${username}" type="text" name="user" class="form-control" id="username" aria-describedby="emailHelp">
    </div>
    <button type="submit" id="submit-btn" class="btn btn-primary">Submit</button>
  </div>`;
  formdiv.addEventListener("click", (event) => {
    let setname = document.querySelector("#username");
    localStorage.setItem("username", setname.value);
    if (event.target.className == "addform") {
      formdiv.style.display = "none";
    }
  });
});

const deleteIdea = (id) => {
  const csrf = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("csrftoken="))
    .split("=")[1];
  console.log(csrf);
  fetch(`deleteidea/${id}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": `${csrf}` },
  });
  location.reload();
};

const editDone = (id) => {
  const csrf = document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("csrftoken="))
    .split("=")[1];
  console.log(csrf);
  fetch(`editidea/${id}/`, {
    method: "POST",
    headers: { "X-CSRFToken": `${csrf}` },
  });
  location.reload();
};

const editIdea = (id) => {
  fetch(`editidea/${id}/`)
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      let formdiv = document.querySelector(".addform");
      formdiv.style.display = "flex";
      let form = document.querySelector("#addideaform");
      let hidediv = document.querySelector(".hidediv");
      form.style.display = "flex";
      form.action = `editidea/${id}/`;
      hidediv.innerHTML = `<div id="formdiv"
      <div class="mb-3">
      <label for="ideatitle" class="form-label">Idea Title</label>
      <input type="text" value="${data.title}" name="title" class="form-control" id="ideatitle" aria-describedby="emailHelp">
      </div>
      <div class="mb-3">
      <label for="ideadesc" class="form-label">Idea Description</label>
      <textarea type="text" name="description" class="form-control" id="ideadesc">${data.description}</textarea>
      </div>
      <div class="mb-3">
      <label for="username" class="form-label">Username</label>
      <input value="${data.user}" type="text" name="user" class="form-control" id="username" aria-describedby="emailHelp">
      </div>
      <button type="submit" id="submit-btn" class="btn btn-primary">Edit</button>
    </div>`;
      formdiv.addEventListener("click", (event) => {
        let setname = document.querySelector("#username");
        localStorage.setItem("username", setname.value);
        if (event.target.className == "addform") {
          formdiv.style.display = "none";
        }
      });
    });
};
