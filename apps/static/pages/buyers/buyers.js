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
