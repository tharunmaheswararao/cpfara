let accountDetailsTag = document.getElementsByClassName("account-details")[0];
let accountImgTag = document.getElementsByClassName("account-img")[0];
let usernameElement = document.getElementsByClassName("username")[0];
let emailElement = document.getElementsByClassName("email")[0]
let isAccountDetailsVisisble = false;

const navigateToEventsPage = (event) => {
    return window.location.href = '/events'
}

const navigateToAicte = (event) => {
    return window.location.href = '/institute/aicte'
}

const navigateToIIT = (event) => {
    return window.location.href = '/institute/iit'
}

const navigateToIIITA = (event) => {
    return window.location.href = '/institute/iiita'
}

const navigateToVIT = (event) => {
    return window.location.href = '/institute/vit'
}

const navigateToSRM = (event) => {
    return window.location.href = '/institute/srm'
}

const navigateToSAEC = (event) => {
    return window.location.href = '/institute/saec'
}

const navigateToSubscribe = (event) => {
    return window.location.href = '/subscribe'
}

const navigateToHome = (event) => {
    return window.location.href = '/home'
}

const navigateToLogin = (event) => {
    localStorage.setItem('username', '')
    return window.location.href = '/login'
}

let username = localStorage.getItem('username');

let data = {
    username
}

const displayAccountDetails = (event) => {

    if(isAccountDetailsVisisble) {
        accountDetailsTag.style.display = "none";
        accountImgTag.style.color = "white";
    } else {
        accountDetailsTag.style.display = "block";
        accountImgTag.style.color = "#09f";
        userinfoApi(data);
    }

    isAccountDetailsVisisble = !isAccountDetailsVisisble;

}

function userinfoApi(data) {

    fetch('/api/user/user-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            const keys = Object.keys(data.user_data);
            console.log(keys);
            usernameElement.innerText = data.user_data[0];
            emailElement.innerText = data.user_data[1];
        } else if (data.error) {
            alert('Error signing up: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}
