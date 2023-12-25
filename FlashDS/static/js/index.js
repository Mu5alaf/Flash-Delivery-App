function onVerify(idToken) {
    // Create form
    var form = document.createElement("form");
    form.method = "POST";
    form.style.display = "none";  // Hide form

    // Create and append input elements
    var inputs = [
        { name: "id_token", value: idToken },
        { name: "action", value: "update_user_phone" },
        { name: "csrfmiddlewaretoken", value: getCookie('csrftoken') }
        // Get CSRF token from cookies
    ];

    inputs.forEach(function (inputData) {
        var input = document.createElement("input");
        input.name = inputData.name;
        input.value = inputData.value;
        form.appendChild(input);
    });

    // Append form to body and submit
    document.body.appendChild(form);
    form.submit();
}

// Function to get cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// To use the visible reCAPTCHA widget, create an element on your page to 
// contain the widget, and then create a RecaptchaVerifier object, specifying the 
// ID of the container when you do so. For example:
document.addEventListener('DOMContentLoaded', function () {
    // Clear inner elements of the reCAPTCHA container
    var recaptchaContainer = document.getElementById('recaptcha-container');
    recaptchaContainer.innerHTML = '';

    // Create the RecaptchaVerifier object
    window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
        size: "invisible"
    });
})
// To initiate phone number sign-in, present the user an interface that prompts them to provide 
// their phone number, and then call signInWithPhoneNumber to request that Firebase send an 
// authentication code to the user's phone by SMS:
$("#send-code button").on('click', function () {
    const PhoneNum = $("#send-code input").val();
    console.log(PhoneNum);
    firebase.auth().signInWithPhoneNumber(PhoneNum, window.recaptchaVerifier)
        .then((confirmationResult) => {
            console.log(confirmationResult);
            window.confirmationResult = confirmationResult;
            $("#send-code").addClass("d-none");
            $("#Verify-code").removeClass("d-none");
        }).catch((error) => {
            // Error; SMS not sent
            alertify.set('notifier', 'position', 'top-center');
            alertify.error('Something went wrong');
        });
});
// Sign in the user with the verification code
$("#Verify-code button").on('click', function () {
    const verify = $("#Verify-code input").val();

    confirmationResult.confirm(verify).then((result) => {
        // User signed in successfully.
        const user = result.user;
        console.log(user.PhoneNum);
        // ...
        user.getIdToken().then(function (idToken) {
            onVerify(idToken)
        });
    }).catch((error) => {
        // User couldn't sign in (bad verification code?)
        alertify.set('notifier', 'position', 'top-center');
        alertify.error('Something went wrong');
    });

});

$("#change_phone button").on('click', function () {
    $("#change_phone").addClass("d-none");
    $("#send-code").removeClass("d-none");
})

