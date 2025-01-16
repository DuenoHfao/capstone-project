const signInButtonElement = document.getElementById('sign-in-btn');
const loginEmailInputElement = document.getElementById('login-user-email');
const loginPasswordInputElement = document.getElementById('login-user-password');
const signInEmailErrorMessage = document.getElementById('email-error-message');
const signUpEmailInputElement = document.getElementById('signup-email-input');
const signUpPasswordInputElement = document.getElementById('signup-password-input');
const signUpCreateAccountButton = document.getElementById('create-account-btn');

console.log(signInButtonElement);

signInButtonElement.addEventListener('click', (event) => {
    let userInputEmail = loginEmailInputElement.value;

    // if user input for email is empty
    if (!userInputEmail) {
        signInEmailErrorMessage.innerHTML = "Email cannot be empty";
        return;
    }
    else {
        signInEmailErrorMessage.innerHTML = "";
    }

    let userInputPassword = loginPasswordInputElement.value;

    $.ajax({
        url: "/login",
        type: "POST",
        data: {
            email: userInputEmail,
            password: userInputPassword
        },
        success: function (navigation) {
            window.location.href = navigation;
        },
        error: function (message) {
            alert(message)
        }
    })
});

console.log(signUpCreateAccountButton);

signUpCreateAccountButton.addEventListener('click', (event) => {

    let signUpUserInputEmail = signUpEmailInputElement.value;

    if (!signUpUserInputEmail) {
        signUpEmailErrorMessage.innerHTML = "Email cannot be empty";
        return;
    }
    else {
        signUpEmailErrorMessage.innerHTML = "";
    }

    let signUpUserInputPassword = signUpPasswordInputElement.value;

    $.ajax({
        url: "/signup",
        type: "POST",
        data: {
            email: signUpUserInputEmail,
            password: signUpUserInputPassword
        },
        success: function (navigation) {
            console.log(navigation)
            // window.location.href = navigation;
        },
        error: function (message) {
            alert(message)
        }
    })
})