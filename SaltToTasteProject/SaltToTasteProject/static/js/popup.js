let btnSign = document.querySelector(".shine-button_signin");

btnSign.onclick = () => {
    let popupUp = document.querySelector(".signup__popup");
	let popupIn = document.querySelector(".signin__popup");
	let btnSignin = document.querySelector(".btn__signin");
	let popup = document.querySelector(".sign__container");
	popup.classList.add("sign__container_active");
    popupIn.classList.add("signin__popup_active");
    btnSignin.classList.add("btn__signin_active");

	let btnSignup = document.querySelector(".btn__signup");
	btnSignup.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.add("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.add("btn__signup_active");
	}

	btnSignin.onclick = () => {
	popupUp.classList.remove("signup__popup_active");
	popupIn.classList.add("signin__popup_active");
	btnSignup.classList.remove("btn__signup_active");
	btnSignin.classList.add("btn__signin_active");
	}
	let btnExit = document.querySelector(".sign_background");
	let btnX = document.querySelector(".cl-btn-7");
	btnX.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.remove("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.remove("btn__signup_active");
 	popup.classList.remove("sign__container_active");
 }
	btnExit.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.remove("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.remove("btn__signup_active");
 	popup.classList.remove("sign__container_active");
 }
}
/*---------------------------------------------------------------*/

let btnAddCollections = document.querySelector(".collection__item-create");
btnAddCollections.onclick = () => {
	let popupAddCollections = document.querySelector(".popup__add_collections-container");
	popupAddCollections.classList.add("popup__add_collections-container_active");

	let btnAddCollectionsClose = document.querySelector(".add_collections__btn-close");
	btnAddCollectionsClose.onclick = () => {
	popupAddCollections.classList.remove("popup__add_collections-container_active");
    }
    let btnBackgroundClose = document.querySelector(".popup__add_collections-background");
	btnBackgroundClose.onclick = () => {
	popupAddCollections.classList.remove("popup__add_collections-container_active");
    }
}