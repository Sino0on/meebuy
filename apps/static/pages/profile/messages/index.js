const chatItems = document.querySelectorAll('.card__item');

chatItems.forEach((item) => {
  item.addEventListener('click', (e) => {
    if (e.target.classList.contains('threeDots')) {
      e.preventDefault();
        const dropdownContent = e.target.nextElementSibling;

        dropdownContent.classList.toggle("hidden");
    }
  });
});