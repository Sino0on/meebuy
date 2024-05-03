// heart
const heart = document.querySelector('#heart');

// sliders
const slider = new Swiper('.product__slider', {
  slidesPerView: 3,
  spaceBetween: 10,
  navigation: {
    nextEl: '.content-prev',
    prevEl: '.content-next',
  },
});

const slider2 = new Swiper('.swiper__banner', {
  slidesPerView: 1,
  spaceBetween: 10,
  navigation: {
    nextEl: '.banner-next',
    prevEl: '.banner-prev',
  },
});

// heart
const toggleActive = () => {
  heart.classList.toggle('text-logo-color');
};

heart.addEventListener('click', toggleActive);
