const toggles = document.querySelectorAll('.accordion-toggle');

toggles.forEach((toggle) => {
  toggle.addEventListener('click', function () {
    const content = this.nextElementSibling;
    const arrow = this.querySelector('.arrow');

    // Проверяем, активен ли уже аккордеон
    if (content.style.height && content.style.height !== '0px') {
      content.style.height = '0px';
      content.style.opacity = '0';
      arrow.classList.remove('rotate-90');
      arrow.classList.add('-rotate-90');
    } else {
      content.style.height = content.scrollHeight + 'px';
      content.style.opacity = '1';
      arrow.classList.add('rotate-90');
      arrow.classList.remove('-rotate-90');
    }
  });
});
