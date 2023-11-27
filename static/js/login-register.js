function validate_password(password) {
    if (password.length < 8) {
        return 'password must be at least 8 characters long'
    }

    if (!/[a-z]/.test(password)) {
        return 'Password must include both lower and upper case characters.'
    }

    if (!/[A-Z]/.test(password)) {
        return 'Pasword must include both lower and upper case characters.'
    }

    if (!/\d/.test(password)) {
        return 'password must include at least one number.'
    }
    if (!/[!@#$%^&*()_?.,+=/\\`~-]/.test(password)) {
        return 'password must include at least one symbol.'
    }
    return 'valid';
}

document.addEventListener("DOMContentLoaded", function () {
    
    const username = document.getElementById("user-name");
    const password = document.getElementById("password");
    const confirm_password = document.getElementById("confirm-password");
    let submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.style.opacity = '.5'
    

    const username_tip = document.getElementById("username-tip");
    const password_tip = document.getElementById("password-tip");
    const confirm_tip = document.getElementById("confirm-tip");


    let valid_username = false;
    let valid_password = false;
    let valid_confirmation = false;

    username.addEventListener("input", function () {
        if (username.value.length > 25) { 
            username_tip.innerHTML = 'Username must be 25 charactars or less.';
            valid_username = false;
        }
        else {
            username_tip.innerHTML = '';
            valid_username = true;
        }
        updateSubmitButtonState(valid_username, valid_password, valid_confirmation)
    });

    password.addEventListener("input", function () {
        var msg = validate_password(password.value);
        if (msg != 'valid') {
            password_tip.innerHTML = msg;
            valid_password = false;
        } else {
            password_tip.innerHTML = '';
            valid_password = true;
        }
        updateSubmitButtonState(valid_username, valid_password, valid_confirmation)
    });

    confirm_password.addEventListener('input', function () { 
        if (confirm_password.value != password.value) {
            confirm_tip.innerHTML = 'Passwords do not match.';
            valid_confirmation = false;
        } else { 
            confirm_tip.innerHTML = '';
            valid_confirmation = true;
        }
        updateSubmitButtonState(valid_username, valid_password, valid_confirmation)
    });

    function updateSubmitButtonState(rule1, rule2, rule3) {
        if (rule1 && rule2 && rule3) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1'
            submitBtn.style.cursor = 'pointer';
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '.5'
            submitBtn.style.cursor = 'not-allowed';
        }
    }
});