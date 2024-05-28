const burgerMenu = document.querySelector('#burgerMenu');
const burgerIcon = document.querySelector('#burgerIcon');
const closeBurgerIcon = document.querySelector('#closeIcon');


const toggleMenu = () => {
    if (burgerMenu.classList.contains('translate-x-0')) {
        burgerMenu.classList.remove('translate-x-0');
        burgerMenu.classList.add('translate-x-full');
        enableScroll();
    } else {
        disableScroll();
        burgerMenu.classList.add('translate-x-0');
        burgerMenu.classList.remove('translate-x-full');
    }
};

burgerIcon.addEventListener('click', toggleMenu);
closeBurgerIcon.addEventListener('click', toggleMenu);
// search
const searchForm = document.querySelector('#searchForm');
const searchIcon = document.querySelector('#searchIconImg');

const toggleFormWidth = () => {
    searchForm.classList.toggle('w-3/4'); // Используйте toggle для переключения класса
    searchForm.classList.toggle('w-min'); // Используйте toggle для переключения класса
};

searchIcon.addEventListener('click', toggleFormWidth);


function disableScroll() {
    if (window.innerWidth > 992) {
        return;
    }
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden'; // Для поддержки разных браузеров
}

function enableScroll() {
    if (window.innerWidth > 992) {
        return;
    }
    document.body.style.overflow = '';
    document.documentElement.style.overflow = ''; // Возвращаем стандартное поведение
}
