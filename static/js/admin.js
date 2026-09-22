const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("passwordInput");

if (togglePassword && passwordInput) {

    togglePassword.addEventListener("click", function () {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";

            this.innerHTML = '<i class="fas fa-eye-slash"></i>';

        } else {

            passwordInput.type = "password";

            this.innerHTML = '<i class="fas fa-eye"></i>';

        }

    });

}