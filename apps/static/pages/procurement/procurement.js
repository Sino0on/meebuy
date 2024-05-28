// Select
const selectContainer = document.getElementById("selectContainer");
const openIcon = document.querySelector(".openIcon");
const closeIcon = document.querySelector(".closeIcon");
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
    closeIcon.style.display = "block";
  } else {
    selectModal.style.display = "none";
    openIcon.style.display = "block";
    closeIcon.style.display = "none";
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
        closeIcon.style.display = "none";
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

// card read & unread bg-color
const toggleCards = document.querySelectorAll(".cardCont");

const toggleCardHandler = (event) => {
  const card = event.currentTarget;
  if (card.style.backgroundColor === "rgb(235, 235, 235)") {
    card.style.backgroundColor = "#fff";
  } else {
    card.style.backgroundColor = "#ebebeb";
  }
};

toggleCards.forEach((card) => {
  card.addEventListener("click", toggleCardHandler);
});

// like
const hearts = document.querySelectorAll("#heart");

const toggleHeartHandler = (event) => {
  console.log('heart')
  event.stopPropagation();
  const heart = event.currentTarget;
  const insideHeart = heart.querySelector("#inside-heart");
  const borderHeart = heart.querySelector("#border-heart");

  insideHeart.classList.toggle("red");
  heart.classList.toggle("heart-active-color");
  borderHeart.classList.toggle("border-heart");
};

hearts.forEach((heart) => {
  heart.addEventListener("click", toggleHeartHandler);
});

const pagination = document.getElementById("pagination");
const prevPage = document.getElementById("prevPage");
const nextPage = document.getElementById("nextPage");
const prevPagee = document.getElementById("prevPagee");
const nextPagee = document.getElementById("nextPagee");

prevPage.addEventListener("click", goToPreviousPage);
nextPage.addEventListener("click", goToNextPage);
prevPagee.addEventListener("click", goToPreviousPage);
nextPagee.addEventListener("click", goToNextPage);

function goToPreviousPage() {
  const activePage = pagination.querySelector(".active");
  if (activePage.previousElementSibling) {
    activePage.classList.remove("active");
    activePage.previousElementSibling.classList.add("active");
  }
}

function goToNextPage() {
  const activePage = pagination.querySelector(".active");
  if (activePage.nextElementSibling) {
    activePage.classList.remove("active");
    activePage.nextElementSibling.classList.add("active");
  }
}
const currentPageItems = pagination.querySelectorAll(".page");
currentPageItems.forEach((page) => {
  page.addEventListener("click", setCurrentPage);
});

function setCurrentPage(event) {
  currentPageItems.forEach((page) => {
    page.classList.remove("active");
  });

  event.currentTarget.classList.add("active");
}

document.addEventListener("DOMContentLoaded", () => {
  const pagination = document.getElementById("pagination");
  const pages = pagination.querySelectorAll(".page");
  const ellipsis = pagination.querySelectorAll(".ellipsis");

  function updatePagination(currentPageIndex) {
    pages.forEach((page, index) => {
      if (index === currentPageIndex) {
        page.classList.add("active");
      } else {
        page.classList.remove("active");
      }
    });

    ellipsis.forEach((ellipsisItem) => (ellipsisItem.style.display = "none"));
    if (currentPageIndex > 4) {
      ellipsis[0].style.display = "block";
    }
    if (currentPageIndex < pages.length - 5) {
      ellipsis[1].style.display = "block";
    }

    for (let i = 0; i < pages.length; i++) {
      if (i >= currentPageIndex - 2 && i <= currentPageIndex + 2) {
        pages[i].style.display = "block";
      } else {
        pages[i].style.display = "none";
      }
    }
  }

  pages.forEach((page, index) => {
    page.addEventListener("click", () => {
      updatePagination(index);
    });
  });
});

// filter
const filterContainer = document.getElementById("filterContainer");
// const closeFilterContainer = document.getElementById("close-filter-container");
const toggleFilter = document.getElementById("toggleFilter");
const openFilter = document.getElementById("openFilter");

const toggleFilterModal = () => {
  openFilter.style.display =
    openFilter.style.display === "none" ? "block" : "none";
};
const toggleCloseFilterModal = () => {
  openFilter.style.display = "none";
};

filterContainer.addEventListener("click", toggleFilterModal);
// closeFilterContainer.addEventListener("click", toggleCloseFilterModal);

document.addEventListener("click", (event) => {
  if (
    openFilter.style.display === "block" &&
    !filterContainer.contains(event.target) &&
    !openFilter.contains(event.target)
  ) {
    openFilter.style.display = "none";
  }
});
