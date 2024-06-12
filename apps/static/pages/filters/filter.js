// Select
const selectContainer = document.getElementById('selectContainer');
const openIcon = document.querySelector('.openIcon');
const closeIconn = document.querySelector('.closeIcon');
const selectModal = document.getElementById('selectModal');
const selectedSort = selectModal.querySelectorAll('.selected');
const recommendedList = document.getElementById('recommended-list');
const recommended = document.getElementById('recommended');
const newSelectList = document.getElementById('new-list');
const newSelect = document.getElementById('new');

const url = new URL(window.location.href);
const urlParam = url.searchParams.get('order');

if (urlParam) {
  const selecetedContainerText = selectContainer.querySelector('p');
  selecetedContainerText.innerHTML = getTextParam(urlParam);
}

function getTextParam(key) {
  if (key === '-is_new') {
    return 'Новые';
  }
  if (key === '-is_recommended') {
    return 'Рекомендуемые';
  }
}

const toggleSelectModal = () => {
  if (
    selectModal.style.display === 'none' ||
    selectModal.style.display === ''
  ) {
    selectModal.style.display = 'block';
    openIcon.style.display = 'none';
    closeIconn.style.display = 'block';
  } else {
    selectModal.style.display = 'none';
    openIcon.style.display = 'block';
    closeIconn.style.display = 'none';
  }
};
const checkedSelect = element => {
  const select = [recommended, newSelect];
  for (let i = 0; i < select.length; i++) {
    if (select[i] === element) {
      select[i].style.display = 'block';
      setTimeout(() => {
        selectModal.style.display = 'none';
        openIcon.style.display = 'block';
        closeIconn.style.display = 'none';
      }, 200);
    } else {
      select[i].style.display = 'none';
    }
  }
};
document.addEventListener('DOMContentLoaded', function () {
  selectedSort.forEach(function (item) {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const text = item.textContent;
      changeButtonText(text);
    });
  });
});

function changeButtonText(text) {
  selectContainer.querySelector('p').textContent = text;
}

function updateURL(key, value) {
  const url = new URL(window.location.href);
  url.searchParams.set(key, value);
  window.location.href = url.toString();
}

recommendedList.addEventListener('click', () => {
  checkedSelect(recommended);
  updateURL('order', '-is_recommended');
});
newSelectList.addEventListener('click', () => {
  checkedSelect(newSelect);
  updateURL('order', '-is_new');
});
selectContainer.addEventListener('click', toggleSelectModal);

/// filter
const filterContainer = document.getElementById('filterContainer');
const toggleFilter = document.getElementById('toggleFilter');
const openFilter = document.getElementById('openFilter');
const filterBtn = document.getElementById('filterBtn');

const toggleFilterModal = () => {
  openFilter.style.display =
    openFilter.style.display === 'none' ? 'block' : 'none';
};

const toggleCloseFilterModal = event => {
  if (
    openFilter.style.display === 'block' &&
    !filterContainer.contains(event.target) &&
    !openFilter.contains(event.target)
  ) {
    return (openFilter.style.display = 'none');
  }
};
filterBtn.addEventListener('click', e => {
  toggleCloseFilterModal();
});

openFilter.addEventListener('click', e => {
  e.stopPropagation();
  if (e.target == e.currentTarget) {
    toggleCloseFilterModal();
  }
});

filterContainer.addEventListener('click', toggleFilterModal);

document.addEventListener('click', event => {
  event.stopPropagation();
  if (
    openFilter.style.display === 'block' &&
    !filterContainer.contains(event.target) &&
    !openFilter.contains(event.target)
  ) {
    return (openFilter.style.display = 'none');
  }
});

document
  .getElementById('filterContainer')
  .addEventListener('click', function () {
    this.classList.toggle('active');
  });

// delete buyers block

document.addEventListener('click', function (event) {
  if (event.target.closest('.delete-button')) {
    const country = event.target.closest('.country');
    if (country) {
      country.remove();
    }
  }
});

const countrySelect = document.getElementById("country-options");
  const regionSelect = document.getElementById("region-options");
  const citySelect = document.getElementById("city-options");

  function transformData(data) {
  const transformed = {};

  data.forEach(country => {
    const countryObj = {};

    country.regions.forEach(region => {
      const regionObj = {};

      region.cities.forEach(city => {
        regionObj[city.title] = city.title;
      });

      countryObj[region.title] = regionObj;
    });

    transformed[country.title] = countryObj;
  });

  return transformed;
}

  const formattedString = openFilter.getAttribute("data-countries").replace(/'/g, '"');
  const countries = JSON.parse(formattedString);
  const transformedData = transformData(countries);
  addOptions(regionSelect,transformedData[countrySelect.value])
  addOptions(citySelect,transformedData[countrySelect.value][regionSelect.value])


  countrySelect.addEventListener('change',(e)=>{
    const selectedCountry = e.target.value;
    addOptions(regionSelect,transformedData[selectedCountry])
    addOptions(citySelect,transformedData[selectedCountry][regionSelect.value])
  })

  regionSelect.addEventListener('change',(e)=>
  {
    const selectedRegion = e.target.value;
    addOptions(citySelect,transformedData[countrySelect.value][selectedRegion])
  })

  function addOptions(element,options){
    element.innerHTML = ""
    for(const option in options){
    const optionEl = document.createElement("option");
      optionEl.textContent = option;
      optionEl.value = option;
      element.appendChild(optionEl);
    }
  }