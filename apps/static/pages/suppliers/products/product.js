const swiper = new Swiper(".swiper1", {
  slidesPerView: 3,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

});

function getDirection() {
  var direction = window.innerWidth <= 730 ? "horizontal" : "horizontal";

  return direction;
}

const swiper2 = new Swiper(".swiper2", {
  slidesPerView: window.innerWidth >= 992 ? 4 : 2,
  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  pagination: {
    el: window.innerWidth >= 992 ? ".swiper-pagination" : "",
    clickable: true,
  },
});
// burger menu
const burgerMenu = document.querySelector("#burgerMenu");
const burgerIcon = document.querySelector("#burgerIcon");
const closeIcon = document.querySelector("#closeIcon");
// search
const searchForm = document.querySelector("#searchForm");
const searchIcon = document.querySelector("#searchIconImg");

const toggleMenu = () => {
  if (burgerMenu.classList.contains("translate-x-0")) {
    burgerMenu.classList.remove("translate-x-0");
    burgerMenu.classList.add("translate-x-full");
  } else {
    burgerMenu.classList.add("translate-x-0");
    burgerMenu.classList.remove("translate-x-full");
  }
};

burgerIcon.addEventListener("click", toggleMenu);
closeIcon.addEventListener("click", toggleMenu);

const toggleFormWidth = () => {
  searchForm.classList.toggle("w-3/4"); // Используйте toggle для переключения класса
  searchForm.classList.toggle("w-min"); // Используйте toggle для переключения класса
};

searchIcon.addEventListener("click", toggleFormWidth);

const slider = new Swiper(".swiper2", {
  pagination: {
    el: ".pagination2",
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

const hearts = document.querySelectorAll(".heart");
hearts.forEach((heart) => {
  heart.addEventListener("click", toggleActiveHeart);
});

function toggleActiveHeart(event) {
  event.currentTarget.classList.toggle("text-logo-color");
}


const mainImage = document.getElementById("main-image");
const thumbnailImages = document.querySelectorAll("#thumbnails .swiper-slide")

thumbnailImages.forEach(thumb => {
  thumb.addEventListener("click", () => {
    mainImage.src = thumb.querySelector("img").src
  })
})