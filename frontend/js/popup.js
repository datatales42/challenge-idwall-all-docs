const menuHamburger = document.querySelector('.menu_hamburger');
const menuPopup = document.getElementById('menuPopup');

menuHamburger.addEventListener('click', () => {
    menuPopup.style.display = 'block';
});

menuPopup.addEventListener('click', () => {
    menuPopup.style.display = 'none';
});
