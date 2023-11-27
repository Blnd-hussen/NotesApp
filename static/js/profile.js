document.addEventListener('DOMContentLoaded', function () { 

    const optionSwitcher = document.getElementById('optionSwitcher');
    const headerMsg = document.getElementById('headerMsg');
    const form = document.getElementById('form');
    const newPasswordInput = document.getElementById('newPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const submitBtn = document.getElementById('submitBtn');


    optionSwitcher.addEventListener('click', function () {
        if (submitBtn.innerHTML == 'Update') {
            headerMsg.innerHTML = 'Delete Account';
            newPasswordInput.remove();
            confirmPasswordInput.remove();
            submitBtn.innerHTML = 'Delete Account';
            submitBtn.value = "deleteUser";
            optionSwitcher.innerHTML = 'Update Password';
        } else {
            headerMsg.innerHTML = 'Update Password';
            form.removeChild(submitBtn);
            form.appendChild(newPasswordInput);
            form.appendChild(confirmPasswordInput);
            form.appendChild(submitBtn);
            submitBtn.innerHTML = 'Update';
            submitBtn.value = "updatePassword";
            optionSwitcher.innerHTML = 'Delete Account';
        }


    });
});