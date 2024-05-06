let heartIcons = document.querySelectorAll('.heart__icon');
// category sidebar
const categoryCloseIcon = document.querySelector('#categoryCloseIcon');
const categoryMenu = document.querySelector('#categoryMenu');
const categoryBtn = document.querySelector('#categoryBtn');

// burger menu
const burgerMenu = document.querySelector('#burgerMenu');
const burgerIcon = document.querySelector('#burgerIcon');
const closeIcon = document.querySelector('#closeIcon');

// heart icon
heartIcons.forEach((heartIcon) => {
  heartIcon.addEventListener('click', () => {
    heartIcon.classList.toggle('active');
  });
});

// window scroll
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

const toggleCategoryMenu = () => {
  if (categoryMenu.classList.contains('-translate-x-full')) {
    categoryMenu.classList.remove('-translate-x-full');
    categoryMenu.classList.add('translate-x-0');
    disableScroll();
  } else {
    categoryMenu.classList.add('-translate-x-full');
    categoryMenu.classList.remove('translate-x-0');
    enableScroll();
  }
};

categoryBtn.addEventListener('click', toggleCategoryMenu);
categoryCloseIcon.addEventListener('click', toggleCategoryMenu);

const toggleMenu = () => {
  if (burgerMenu.classList.contains('translate-x-0')) {
    burgerMenu.classList.remove('translate-x-0');
    burgerMenu.classList.add('translate-x-full');
  } else {
    burgerMenu.classList.add('translate-x-0');
    burgerMenu.classList.remove('translate-x-full');
  }
};

burgerIcon.addEventListener('click', toggleMenu);
closeIcon.addEventListener('click', toggleMenu);
