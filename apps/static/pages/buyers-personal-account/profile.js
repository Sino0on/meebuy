// avatar upload
const avatarInput = document.querySelector('#upload');
const avatar = document.querySelector('#avatar');

avatarInput.addEventListener('change', () => {
    const reader = new FileReader();
    reader.readAsDataURL(avatarInput.files[0]);
    reader.addEventListener('load', () => {
        avatar.src = reader.result;
    });
})

// dropdown
const dropdownBtn = document.querySelector('.dropdown__btn');
const dropdownMenu = document.querySelector('.dropdown__menu');

dropdownBtn.addEventListener('click', () => {
    const isActive = dropdownMenu.classList.contains('active');
    dropdownMenu.style.maxHeight = isActive ? "0" : `${dropdownMenu.scrollHeight}px`;
    dropdownMenu.classList.toggle('active');
})

// tabs
function openTab(_, tabId) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.style.display = 'none';
    });

    const allTabs = document.querySelectorAll('.tabs__item');
    allTabs.forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(tabId).style.display = 'block';
    const activeTab = Array.from(allTabs).find(tab => tab.onclick.toString().includes(`'${tabId}'`));
    if (activeTab) {
        activeTab.classList.add('active');
    }
}