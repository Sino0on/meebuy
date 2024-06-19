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
    const searchListEl = document.getElementById('searchList')

    getDeleteBtns()

    function getSearchListItem(option) {
        const li = document.createElement("li")
        const h3 = document.createElement("h3")
        const p = document.createElement('p')
        const cityEl = document.createElement('p')
        const flexDiv = document.createElement('div')
        const coverDiv = document.createElement('a')

        const deleteDiv = document.createElement('div');
        deleteDiv.setAttribute('data-id', option.id)
        deleteDiv.classList.add('delete-option-btn')
        const img = document.createElement('img')

        img.src = "/static/assets/images/icons/trash.svg";

        flexDiv.classList.add('flex', 'flex-row', 'justify-between', 'w-full')


        li.classList.add('p-4', 'border-b', 'border-grey-light');
        h3.classList.add('font-semibold');
        p.classList.add('text-sm', 'text-grey-dark');


        deleteDiv.setAttribute('data-id', option.id)
        deleteDiv.style.cursor = 'pointer'
        h3.textContent = option.name;
        cityEl.textContent = option.city;
        p.textContent = option.date;

        coverDiv.href = `/search/detail/${option.id}`

        deleteDiv.appendChild(img)
        coverDiv.appendChild(h3);
        coverDiv.appendChild(cityEl)
        coverDiv.appendChild(p);

        flexDiv.appendChild(coverDiv)
        flexDiv.appendChild(deleteDiv)
        li.appendChild(flexDiv)

        return li;
    }


    const formattedString = optionsList.getAttribute("data-options").replace(/'/g, '"');
    const optionsData = JSON.parse(formattedString);

    console.log(optionsData)

    selectButton?.addEventListener("click", () => {
        optionsList.classList.toggle("hidden");
    });

    const forMonth = 'За месяц';
    const forWeek = 'За неделю';
    const forYear = 'За год';

    function getFilteredOptions(filterOption) {
        if (filterOption === forYear) {
            return optionsData.filter((item) => item.range === forYear || item.range === forWeek || item.range === forMonth)
        } else if (filterOption === forMonth) {
            return optionsData.filter((item) => item.range === forWeek || item.range === forMonth)
        } else if (filterOption === forWeek) {
            return optionsData.filter((item) => item.range === forWeek)
        } else {
            return optionsData;
        }
    }

    options?.forEach((option) => {
        option.addEventListener("click", () => {
            const selectedValue = option.getAttribute("data-value");
            selectedOptionText.textContent = selectedValue;
            hiddenSelectedOption.value = selectedValue;
            optionsList.classList.add("hidden");

            searchListEl.innerHTML = '';

            const filteredData = getFilteredOptions(selectedValue);

            filteredData.forEach(filteredOption => {
                const element = getSearchListItem(filteredOption)
                searchListEl.appendChild(element)
            })

            getDeleteBtns();


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

const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

function getDeleteBtns() {
    const deleteBtns = document.querySelectorAll('.delete-option-btn');

    deleteBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            deleteItem(btn.getAttribute('data-id'));

            btn.closest('li').remove()
        })
    })
}

async function deleteItem(id) {
    const host = document.location.host;

    const res = await fetch(`/search/delete/${id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })

    return res;
}



