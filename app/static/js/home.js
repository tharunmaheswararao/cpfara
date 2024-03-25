let accountDetailsTag = document.getElementsByClassName("account-details")[0];
let accountImgTag = document.getElementsByClassName("account-img")[0];
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

const navigateToSRM = (event) => {
    return window.location.href = '/institute/srm'
}

const navigateToSubscribe = (event) => {
    return window.location.href = '/subscribe'
}

const navigateToHome = (event) => {
    return window.location.href = '/home'
}



const displayAccountDetails = (event) => {

    if(isAccountDetailsVisisble) {
        accountDetailsTag.style.display = "none";
        accountImgTag.style.color = "white";
    } else {
        accountDetailsTag.style.display = "block";
        accountImgTag.style.color = "#09f";
    }

    isAccountDetailsVisisble = !isAccountDetailsVisisble;

}
