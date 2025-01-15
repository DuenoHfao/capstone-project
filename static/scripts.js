const signInButtonElement = document.getElementById('sign-in-btn');
const loginEmailInputElement = document.getElementById('email-input');
const loginPasswordInputElement = document.getElementById('password-input');
const signInEmailErrorMessage = document.getElementById('email-error-message');


signInButtonElement.addEventListener('click', (event) => {
    let userInputEmail = loginEmailInputElement.value;

    // if user input for email is empty
    if (!userInputEmail) {
        signInEmailErrorMessage.innerHTML = "Email cannot be empty";
        return;
    }

    let userInputPassword = loginPasswordInputElement.value;
    $.ajax({url:'/login',
        type: "POST"
    });
})