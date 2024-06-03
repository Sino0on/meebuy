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
const tenderHearts = document.querySelectorAll("#heart");

const toggleHeartHandler = (event) => {
  event.stopPropagation();
  const heart = event.currentTarget;
  const insideHeart = heart.querySelector("#inside-heart");
  const borderHeart = heart.querySelector("#border-heart");

  insideHeart.classList.toggle("red");
  heart.classList.toggle("heart-active-color");
  borderHeart.classList.toggle("border-heart");
};

tenderHearts.forEach((heart) => {
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

/// filter

// const filterContainer = document.getElementById("filterContainer");
// const toggleFilter = document.getElementById("toggleFilter");
// const openFilter = document.getElementById("openFilter");
// const filterBtn = document.getElementById("filterBtn");

// const toggleFilterModal = () => {
//   openFilter.style.display =
//     openFilter.style.display === "none" ? "block" : "none";
// };
// const toggleCloseFilterModal = () => {
//   openFilter.style.display = "none";
// };

// filterBtn.addEventListener("click", (e) => {
//   e.preventDefault();
//   toggleCloseFilterModal();
// });

// openFilter.addEventListener("click", (e) => {
//   e.stopPropagation();
//   if (e.target == e.currentTarget) {
//     toggleCloseFilterModal();
//   }
// });

// filterContainer.addEventListener("click", toggleFilterModal);

// document.addEventListener("click", (event) => {
//   event.stopPropagation();
//   if (
//     openFilter.style.display === "block" &&
//     !filterContainer.contains(event.target) &&
//     !openFilter.contains(event.target)
//   ) {
//     return (openFilter.style.display = "none");
//   }
// });

// document
//   .getElementById("filterContainer")
//   .addEventListener("click", function () {
//     this.classList.toggle("active");
//   });
