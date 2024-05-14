// photos upload
const fileInputs = document.querySelectorAll(".photos__input");

function handleFileLoad(event, index) {
  const imageElement = document.getElementById(`preview${index + 1}`);
  imageElement.src = event.target.result;
  imageElement.classList.remove("hidden");
  const iconElement = document.getElementById(`icon${index + 1}`);
  iconElement.style.display = "none";
}

fileInputs.forEach((input, index) => {
  input.addEventListener("change", () => {
    const file = input.files[0];
    if (file) {
      console.log(input.id.substring(4));
      const reader = new FileReader();
      reader.onload = function(event) {
        handleFileLoad(event, index);
      };
      reader.readAsDataURL(file);
    }
  });
});

// period

const periodItems = document.querySelectorAll(".period__item");

periodItems.forEach((item) => {
  item.addEventListener("click", () => {
    periodItems.forEach((item) => {
      item.classList.remove("active");
    });
    item.classList.add("active");
  });
});