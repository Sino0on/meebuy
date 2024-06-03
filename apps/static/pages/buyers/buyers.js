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
