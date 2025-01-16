const signInButtonElement = document.getElementById('sign-in-btn');
const loginEmailInputElement = document.getElementById('login-user-email');
const loginPasswordInputElement = document.getElementById('login-user-password');
const signInEmailErrorMessage = document.getElementById('email-error-message');
const signUpEmailInputElement = document.getElementById('signup-email-input');
const signUpPasswordInputElement = document.getElementById('signup-password-input');
const signUpCreateAccountButtonElement = document.getElementById('create-account-btn');
const signUpEmailErrorMessage = document.getElementById('email-error-message');
const deleteAccountButtonElement = document.getElementById('delete-account-btn');


if (signInButtonElement) {
    signInButtonElement.addEventListener('click', (event) => {
        console.log("Sign in button clicked");
        let userInputEmail = loginEmailInputElement.value;
    
        // if user input for email is empty
        if (!userInputEmail) {
            signInEmailErrorMessage.innerHTML = "Email cannot be empty";
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
}



if (signUpCreateAccountButtonElement) {
    signUpCreateAccountButtonElement.addEventListener('click', (event) => {
        console.log("Sign up button clicked");
    
        let signUpUserInputEmail = signUpEmailInputElement.value;
    
        if (!signUpUserInputEmail) {
            signUpEmailErrorMessage.innerHTML = "Email cannot be empty";
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
                window.location.href = navigation;
            },
            error: function (message) {
                alert(message)
            }
        })
    });
}

if (deleteAccountButtonElement) {
    deleteAccountButtonElement.addEventListener('click', (event) => {
        console.log("Delete account button clicked");
    
        $.ajax({
            url: "/delete-account",
            type: "POST",
            success: function (navigation) {
                alert("Account deleted successfully");
                window.location.href = '/';
            },
            error: function (message) {
                alert(message)
            }
        })
    });
}