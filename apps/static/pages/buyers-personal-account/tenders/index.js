// auto search
const addSearchQueryBtns = document.querySelectorAll('.addSearchQuery-btn');
const searchQueryForm = document.querySelector('.form');
const searchQueryFormInput = document.querySelector('.form input[type="text"]');
const emptyContent = document.querySelector('.empty__content');
const filledContent = document.querySelector('.filled__content');

const searchQueryBtnCancel = document.querySelector('#searchQueryBtnCancel');

const searchQueryFormToggle = () => {
    searchQueryForm.classList.toggle('hidden');
    if([].length > 0) {
        return filledContent.classList.toggle('hidden');
    }
    emptyContent.classList.toggle('hidden');
}

addSearchQueryBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        searchQueryFormToggle()
        searchQueryFormInput.focus();
    })
})

searchQueryBtnCancel.addEventListener('click', searchQueryFormToggle)
