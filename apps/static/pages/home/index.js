// burger menu
const burgerMenu = document.querySelector('#burgerMenu');
const burgerIcon = document.querySelector('#burgerIcon');
const closeBurgerIcon  = document.querySelector('#closeIcon');
// search
const searchForm = document.querySelector('#searchForm');
const searchIcon = document.querySelector('#searchIconImg');
// hero search
const heroSearchWrapper = document.querySelector('#heroSearchWrapper');
const heroSearchIconImg = document.querySelector('#heroSearchIconImg');
const heroFormBtn = document.querySelector('#heroFormBtn');
// hero title
const heroTitle = document.querySelector('#heroTitle');
// heart
const hearts = document.querySelectorAll('.heart');

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
closeBurgerIcon.addEventListener('click', toggleMenu);

// search

const toggleFormWidth = () => {
  searchForm.classList.toggle('w-3/4'); // Используйте toggle для переключения класса
  searchForm.classList.toggle('w-min'); // Используйте toggle для переключения класса
};

const heroToggleFormWidth = () => {
  heroFormSearch.classList.toggle('w-3/4'); // Используйте toggle для переключения класса
  heroFormSearch.classList.toggle('w-min'); // Используйте toggle для переключения класса
};

searchIcon.addEventListener('click', toggleFormWidth);
heroSearchIconImg?.addEventListener('click', heroToggleFormWidth);

const itemsToSearch = [
  { label: 'товары', color: 'rgba(228, 219, 0, 1)' },
  { label: 'покупателей', color: 'rgba(254, 67, 145, 1)' },
  { label: 'поставщиков', color: 'rgba(122, 89, 255, 1)' },
  { label: 'производителей', color: 'rgba(0, 192, 181, 1)' },
];

const heroFormToggle = () => {
  const currentWidth = window.innerWidth;
  heroFormBtn.classList.toggle('opacity-0');
  if (currentWidth >= 992) {
    heroSearchWrapper.classList.toggle('w-1/2');
  } else {
    heroSearchWrapper.classList.toggle('w-full');
  }
  setTimeout(() => {
    heroFormBtn.classList.toggle('hidden');
  }, 1500);
};

// Обработчик клика на кнопке "Я ищу"
heroFormBtn?.addEventListener('click', heroFormToggle);

// hero title

const changingTextElement = document.querySelector('#heroTitle');

let currentWordIndex = 0;

function changeWord() {
  if(!changingTextElement) return;
  changingTextElement.style.animation = 'text-out 500ms ease-out';

  setTimeout(() => {
    currentWordIndex = (currentWordIndex + 1) % itemsToSearch.length;
    const currentItem = itemsToSearch[currentWordIndex];

    changingTextElement.textContent = currentItem.label;
    changingTextElement.style.color = currentItem.color;

    changingTextElement.style.animation = 'text-in 500ms ease-out';
  }, 500);
}

setInterval(changeWord, 1500);

changingTextElement ? changingTextElement.style.animation = 'text-in 500ms ease-out' : '';

// slider

const recommendedSlider = new Swiper('.recommended__slider', {
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    992: {
      slidesPerView: 2,
      spaceBetween: 30,
    },
  },
});

const newSlide = new Swiper('.new__slider', {
  navigation: {
    nextEl: '.swiper-button-next-new',
    prevEl: '.swiper-button-prev-new',
  },
  slidesPerView: 2,
  spaceBetween: 30,
  breakpoints: {
    992: {
      slidesPerView: 3,
      spaceBetween: 16,
    },
  },
});

// heart

hearts.forEach(heart => {
    heart.addEventListener('click', () => {
        heart.classList.toggle('text-logo-color');
    });
});

