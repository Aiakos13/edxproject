document.addEventListener("DOMContentLoaded", () => {
  // Tabs staff
  $("#nav-tab a#nav-login-tab").on("click", function (e) {
    e.preventDefault();
    $(this).tab("show");
  });
  $("#nav-tab a#nav-register-tab").on("click", function (e) {
    e.preventDefault();
    $(this).tab("show");
  });

  document.querySelector("#form-register").onsubmit = () => {
    const pass1 = document.querySelector("#reg-password1").value;
    const pass2 = document.querySelector("#reg-password2").value;
    if (pass1 != pass2) {
      alert("Passwords don't match");
      return false;
    }
  };
});
