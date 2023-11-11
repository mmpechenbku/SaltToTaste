let btnSign = document.querySelector(".navbar__item-sign_link");
if (btnSign) {
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
}
/*---------------------------------------------------------------*/

let btnAddCollections = document.querySelector(".collection__item-create");
if (btnAddCollections) {
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
}

/*-----------------------Search Navbar----------------------------*/

let btnSearch = document.querySelector(".navbar__item-search-img");
let searchBox = document.querySelector(".navbar__search-onclick");
btnSearch.onclick = () => {
    if (!searchBox.classList.contains(".navbar__search-onclick_active")) {
        searchBox.classList.add("navbar__search-onclick_active");
    }
    let btnExit = document.querySelector("#nav-search_box")
    btnExit.onblur = () => {
        searchBox.classList.remove("navbar__search-onclick_active");
    }
}


/*----------------------------------------------------------*/
/*-----------------------------Перестроение столбцов---------------------------------*/
if (document.getElementById('large__btn-2')) {
document.getElementById('large__btn-2').addEventListener('click', function rearrangeColumns() {
        var container = document.querySelector('.article-content__container');
        container.classList.toggle('active-2');
        var btnRE = document.querySelector('.article-content__bnt-2');
        btnRE.classList.toggle('active');
});
}
if (document.getElementById('th__btn-3')) {
document.getElementById('th__btn-3').addEventListener('click', function rearrangeColumns() {
        var container = document.querySelector('.article-content__container');
        container.classList.toggle('active-3');
        var btnRE = document.querySelector('.article-content__bnt-3');
        btnRE.classList.toggle('active');
});
}
if (document.getElementById('th-list')) {
document.getElementById('th-list').addEventListener('click', function rearrangeColumns() {
        var container = document.querySelector('.article-content__container');
        container.classList.toggle('active');
        var btnRE = document.querySelector('.article-content__bnt-list');
        btnRE.classList.toggle('active');
});
}
/*----------------------------------------------------------*/
let btn1 = document.getElementById('instructions_steps__btn-id');
let btn2 = document.getElementById('instructions_steps-list-btn-id');
let container1 = document.querySelector('.instructions_steps__btn');
let container2 = document.querySelector('.instructions_steps-list-btn');
<<<<<<< HEAD
if (btn1) {
    container1.classList.add('active');
btn2.addEventListener('click', function () {
    container2.classList.add('active');
    container1.classList.remove('active');
=======
let steps1 = document.querySelector('.instructions_steps');
let steps2 = document.querySelector('.instructions_briefly');
if (btn1) {
    container1.classList.add('active');
    steps1.style.display = 'flex';
    steps2.style.display = 'none';
btn2.addEventListener('click', function () {
    container2.classList.add('active');
    container1.classList.remove('active');
    steps1.style.display = 'none';
    steps2.style.display = 'flex';
>>>>>>> 9bf2ee9438afbe4f14d408b4ee6c38fbe2df49b7

});

btn1.addEventListener('click', function () {
        container1.classList.add('active');
        container2.classList.remove('active');
<<<<<<< HEAD
=======
        steps1.style.display = 'flex';
        steps2.style.display = 'none';
>>>>>>> 9bf2ee9438afbe4f14d408b4ee6c38fbe2df49b7
});
}
