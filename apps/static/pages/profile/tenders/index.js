// auto search
const addSearchQueryBtns = document.querySelectorAll(".addSearchQuery-btn");
const searchQueryForm = document.querySelector(".form");
const searchQueryFormInput = document.querySelector('.form input[type="text"]');
const emptyContent = document.querySelector(".empty__content");
const filledContent = document.querySelector(".filled__content");

const searchQueryBtnCancel = document.querySelector("#searchQueryBtnCancel");

const searchQueryFormToggle = () => {
  searchQueryForm.classList.toggle("hidden");
  if ([].length > 0) {
    return filledContent.classList.toggle("hidden");
  }
  emptyContent.classList.toggle("hidden");
};

addSearchQueryBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    searchQueryFormToggle();
    searchQueryFormInput.focus();
  });
});

searchQueryBtnCancel?.addEventListener("click", searchQueryFormToggle);

document.addEventListener("DOMContentLoaded", () => {
  const selectButton = document.getElementById("selectButton");
  const optionsList = document.getElementById("optionsList");
  const selectedOptionText = document.getElementById("selectedOption");
  const hiddenSelectedOption = document.getElementById("hiddenSelectedOption");
  const options = optionsList?.querySelectorAll("li");

  selectButton?.addEventListener("click", () => {
    optionsList.classList.toggle("hidden");
  });

  options?.forEach((option) => {
    option.addEventListener("click", () => {
      const selectedValue = option.getAttribute("data-value");
      selectedOptionText.textContent = selectedValue;
      hiddenSelectedOption.value = selectedValue;
      optionsList.classList.add("hidden");

      // Submit the form if you want to send the selected option immediately
      // document.getElementById('selectForm').submit();
    });
  });

  // Close the dropdown if clicked outside
  document.addEventListener("click", (event) => {
    if (
      !selectButton?.contains(event.target) &&
      !optionsList?.contains(event.target)
    ) {
      optionsList?.classList.add("hidden");
    }
  });
});
