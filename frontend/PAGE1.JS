// =====================================================
// RESCUEPACK LOGIN
// =====================================================


// =====================================================
// GET HTML ELEMENTS
// =====================================================

const loginForm =
    document.getElementById("loginForm");

const usernameInput =
    document.getElementById("username");

const passwordInput =
    document.getElementById("password");

const errorMessage =
    document.getElementById("errorMessage");

const loginButton =
    document.querySelector(".login-button");


// =====================================================
// LOGIN FORM SUBMISSION
// =====================================================

loginForm.addEventListener(
    "submit",
    async function (event) {

        // Prevent normal form submission
        event.preventDefault();


        // =================================================
        // GET USER INPUT
        // =================================================

        const username =
            usernameInput.value.trim();

        const password =
            passwordInput.value;


        // =================================================
        // CLEAR PREVIOUS MESSAGE
        // =================================================

        errorMessage.textContent = "";

        errorMessage.style.color =
            "#DC2626";


        // =================================================
        // BASIC VALIDATION
        // =================================================

        if (username === "") {

            errorMessage.textContent =
                "Please enter your username.";

            usernameInput.focus();

            return;
        }


        if (password === "") {

            errorMessage.textContent =
                "Please enter your password.";

            passwordInput.focus();

            return;
        }


        // =================================================
        // SHOW LOGIN PROCESS
        // =================================================

        loginButton.disabled = true;

        loginButton.querySelector("span").textContent =
            "Signing in...";


        // =================================================
        // SEND LOGIN REQUEST TO FLASK
        // =================================================

        try {

            const response = await fetch(
                "/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    credentials: "include",

                    body: JSON.stringify({

                        username: username,

                        password: password

                    })
                }
            );


            // =================================================
            // GET SERVER RESPONSE
            // =================================================

            const result =
                await response.json();


            // =================================================
            // LOGIN SUCCESS
            // =================================================

            if (
                response.ok &&
                result.success
            ) {

                errorMessage.textContent =
                    "Login successful. Opening RescuePack...";

                errorMessage.style.color =
                    "#16A34A";


                // =============================================
                // OPEN DASHBOARD
                // =============================================

                setTimeout(function () {

                    window.location.href =
                        "/index.html";

                }, 500);

            }


            // =================================================
            // LOGIN FAILED
            // =================================================

            else {

                errorMessage.textContent =
                    result.message ||
                    "Invalid username or password.";

                errorMessage.style.color =
                    "#DC2626";


                passwordInput.value = "";


                loginButton.disabled = false;

                loginButton.querySelector("span").textContent =
                    "Sign in to RescuePack";


                passwordInput.focus();

            }

        }


        // =================================================
        // SERVER CONNECTION ERROR
        // =================================================

        catch (error) {

            console.error(error);

            errorMessage.textContent =
                "Unable to connect to the server.";

            errorMessage.style.color =
                "#DC2626";


            loginButton.disabled = false;

            loginButton.querySelector("span").textContent =
                "Sign in to RescuePack";

        }

    }
);