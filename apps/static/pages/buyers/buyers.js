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

const checkIcon = document.querySelector(".checkIcon");
const iconGreen = document.querySelectorAll(".iconGreen");

function updatePagination() {
  iconGreen.forEach((page) => {
    if (page.style.stroke === "rgb(43, 41, 44)") {
      page.style.stroke = "green";
    } else if (page.style.stroke === "green") {
      page.style.stroke = "rgb(43, 41, 44)";
    }
  });
}

checkIcon.addEventListener("click", updatePagination);

// filter
const filterContainer = document.getElementById("filterContainer");
const closeFilterContainer = document.getElementById("close-filter-container");
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
closeFilterContainer?.addEventListener("click", toggleCloseFilterModal);

document.addEventListener("click", (event) => {
  if (
    openFilter.style.display === "block" &&
    !filterContainer.contains(event.target) &&
    !openFilter.contains(event.target)
  ) {
    openFilter.style.display = "none";
  }
});
