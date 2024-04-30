// burger menu
const burgerMenu = document.querySelector('#burgerMenu');
const burgerIcon = document.querySelector('#burgerIcon');
const closeIcon = document.querySelector('#closeIcon');
// search
const searchForm = document.querySelector('#searchForm');
const searchIcon = document.querySelector('#searchIconImg');

const heart = document.querySelector('#heart2');
const heart1 = document.querySelector('#heart1');

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

const toggleFormWidth = () => {
  searchForm.classList.toggle('w-3/4'); // Используйте toggle для переключения класса
  searchForm.classList.toggle('w-min'); // Используйте toggle для переключения класса
};

searchIcon.addEventListener('click', toggleFormWidth);

const slider = new Swiper('.supplier__detail-slider', {
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  mousewheel: {
    enabled: true,
    sensitivity: 2,
  },
  breakpoints: {
    992: {
      slidesPerView: 4,
      spaceBetween: 30,
    },
    640: {
      slidesPerView: 2,
      spaceBetween: 30,
    },
  },
});

const toggleActive = () => {
  heart.classList.toggle('text-logo-color');
  heart1.classList.toggle('text-logo-color');
};

heart.addEventListener('click', toggleActive);
heart1.addEventListener('click', toggleActive);
