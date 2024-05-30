// dropdown mobile sort
const dropdownBtn = document.querySelector(".dropdown__btn");
const dropdownMenu = document.querySelector(".dropdown__menu");
const dropdownItems = dropdownMenu.querySelectorAll(".dropdown__item");

const openSort = () => {
  const isActive = dropdownMenu.classList.contains("active");
  dropdownMenu.style.maxHeight = isActive
    ? "0"
    : `${dropdownMenu.scrollHeight}px`;
  dropdownMenu.classList.toggle("active");
};

dropdownBtn.addEventListener("click", openSort);

document.addEventListener("DOMContentLoaded", function () {
  dropdownItems.forEach(function (item) {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      const text = item.textContent;
      changeButtonText(text);
      openSort();
    });
  });
});

function changeButtonText(text) {
  dropdownBtn.querySelector("p").textContent = text;
}

// sort dropdown desktop
const all = document.getElementById("all");
const suppliers = document.getElementById("suppliers");
const manufactures = document.getElementById("manufactures");
const logistics = document.getElementById("logistics");

const toggleSort = (el) => {
  const tab = [all, suppliers, manufactures, logistics];

  for (let i = 0; i <= tab.length; i++) {
    if (tab[i] === el) {
      tab[i].style.backgroundColor = "#fffb98";
    } else {
      tab[i].style.backgroundColor = "";
    }
  }
};
all.addEventListener("click", () => toggleSort(all));
suppliers.addEventListener("click", () => toggleSort(suppliers));
manufactures.addEventListener("click", () => toggleSort(manufactures));
logistics.addEventListener("click", () => toggleSort(logistics));
