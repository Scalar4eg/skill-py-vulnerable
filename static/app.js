const BASE_URL = "/api/";
const API_ENDPOINTS = {
    "LOGIN": "/login-with-password"
}

const getFormData = () => {
    return new FormData(document.forms[0]);
//    const entries = Array.from(form.entries());
//    const payloadJson = entries.reduce((accum, item) => {
//            accum[item[0]] = item[1];
//            return accum;
//        }, {}
//    );
//    return payloadJson;
}


const makeLogin = () => {
    const payload = getFormData();
    const url = BASE_URL + API_ENDPOINTS.LOGIN;
    fetch(url, {method: 'POST', body: payload})
        .then(data => data.json())
        .then(apiResponse => {
            if (apiResponse.result) {
                window.location.href = apiResponse.redirect;
            } else {
                alert("Invalid login or password");
            }
        });
}

window.addEventListener('load', (event) => {
    const passwordInput = document.querySelector("[name=password]");
    passwordInput.addEventListener('keypress', (event) => {
        if (event.code == "Enter") {
            makeLogin();
        }
    });

})