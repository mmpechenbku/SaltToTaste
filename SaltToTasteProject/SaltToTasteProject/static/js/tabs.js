
document.querySelector(".tabs").addEventListener('click', (event) => {
    const linkActive = document.querySelector('.tabs .active');
    const hrefActive = linkActive.getAttribute("href");
    const link = event.target;
    const href = link.getAttribute("href");
    if (linkActive.getAttribute("href") !== href) {
        document.querySelector(href).style.display = 'block';
        document.querySelector(hrefActive).style.display = 'none';
        linkActive.classList.remove('active');
        link.classList.add('active');
    }


});