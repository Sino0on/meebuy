// Select
const selectContainer = document.getElementById("selectContainer");
const openIcon = document.querySelector(".openIcon");
const closeIconn = document.querySelector(".closeIcon");
const selectModal = document.getElementById("selectModal");
const selectedSort = selectModal.querySelectorAll(".selected");
const recommendedList = document.getElementById("recommended-list");
const recommended = document.getElementById("recommended");
const newSelectList = document.getElementById("new-list");
const newSelect = document.getElementById("new");

const toggleSelectModal = () => {
  if (
    selectModal.style.display === "none" ||
    selectModal.style.display === ""
  ) {
    selectModal.style.display = "block";
    openIcon.style.display = "none";
    closeIconn.style.display = "block";
  } else {
    selectModal.style.display = "none";
    openIcon.style.display = "block";
    closeIconn.style.display = "none";
  }
};
const checkedSelect = (element) => {
  const select = [recommended, newSelect];
  for (let i = 0; i < select.length; i++) {
    if (select[i] === element) {
      select[i].style.display = "block";
      setTimeout(() => {
        selectModal.style.display = "none";
        openIcon.style.display = "block";
        closeIconn.style.display = "none";
      }, 200);
    } else {
      select[i].style.display = "none";
    }
  }
};
document.addEventListener("DOMContentLoaded", function () {
  selectedSort.forEach(function (item) {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      const text = item.textContent;
      changeButtonText(text);
      openSort();
    });
  });
});

function changeButtonText(text) {
  selectContainer.querySelector("p").textContent = text;
}

recommendedList.addEventListener("click", () => {
  checkedSelect(recommended);
});
newSelectList.addEventListener("click", () => {
  checkedSelect(newSelect);
});
selectContainer.addEventListener("click", toggleSelectModal);

let heartIcons = document.querySelectorAll(".heart__icon");

// burger menu
const burgerMenu = document.querySelector("#burgerMenu");
const burgerIcon = document.querySelector("#burgerIcon");
const closeIcon = document.querySelector("#closeIcon");

// heart icon
heartIcons.forEach((heartIcon) => {
  heartIcon.addEventListener("click", () => {
    heartIcon.classList.toggle("active");
  });
});

// window scroll
function disableScroll() {
  if (window.innerWidth > 992) {
    return;
  }
  document.body.style.overflow = "hidden";
  document.documentElement.style.overflow = "hidden"; // Для поддержки разных браузеров
}

function enableScroll() {
  if (window.innerWidth > 992) {
    return;
  }
  document.body.style.overflow = "";
  document.documentElement.style.overflow = ""; // Возвращаем стандартное поведение
}

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

// filter

const filterContainer = document.getElementById("filterContainer");
// const closeFilterContainer = document.getElementById("close-filter-container");
const toggleFilter = document.getElementById("toggleFilter");
const openFilter = document.getElementById("openFilter");
const filterBtn = document.getElementById("filterBtn");

const toggleFilterModal = () => {
  openFilter.style.display =
    openFilter.style.display === "none" ? "block" : "none";
};
const toggleCloseFilterModal = () => {
  openFilter.style.display = "none";
};

filterBtn.addEventListener('click', (e) => {
  e.preventDefault();
  toggleCloseFilterModal();
})

openFilter.addEventListener('click', (e) => {
  e.stopPropagation()
  if (e.target == e.currentTarget) {
    toggleCloseFilterModal();
  }
})

filterContainer.addEventListener("click", toggleFilterModal);
// closeFilterContainer.addEventListener("click", toggleCloseFilterModal);

document.addEventListener("click", (event) => {
  event.stopPropagation()
  if (
    openFilter.style.display === "block" &&
    !filterContainer.contains(event.target) &&
    !openFilter.contains(event.target)
  ) {
    return openFilter.style.display = "none";
  }

});

    document.getElementById('filterContainer').addEventListener('click', function() {
      this.classList.toggle('active');
    });
