const goods = document.getElementById('goods');
const category = document.getElementById('category');
const price = document.getElementById('price');
const excelLoader = document.getElementById('excel-loader');
const goodsBlock = document.getElementById('goods-block');
const categoryBlock = document.getElementById('category-block');
const priceBlock = document.getElementById('price-block');
const excelLoaderBlock = document.getElementById('excel-loader-block');

const toggleTab = (element) => {
  const tabs = [goods, category, price, excelLoader];
  const blocks = [goodsBlock, categoryBlock, priceBlock, excelLoaderBlock];
  for (let i = 0; i <= tabs.length; i++) {
    if (tabs[i] === element) {
      tabs[i].style.backgroundColor = '#FFFB98';
      blocks[i].style.display = 'block';
    } else {
      tabs[i].style.backgroundColor ? (tabs[i].style.backgroundColor = '') : '';
      blocks[i].style.display = 'none';
    }
  }
};
goods.addEventListener('click', () => toggleTab(goods));
category.addEventListener('click', () => toggleTab(category));
price.addEventListener('click', () => toggleTab(price));
excelLoader.addEventListener('click', () => toggleTab(excelLoader));

// add category

const buttonAddCategory = document.getElementById('add-category');
const mainSection = document.getElementById('main-section');
const addCategoryBlock = document.getElementById('add-category-block');

const toggleAddCategoryBlock = () => {
  if (mainSection.style.display === 'block') {
    mainSection.style.display = 'none';
    addCategoryBlock.style.display = 'block';
  } else {
    mainSection.style.display = 'block';
    addCategoryBlock.style.display = 'none';
  }
};

buttonAddCategory.addEventListener('click', toggleAddCategoryBlock);
// add goods manually
const buttonAddGoods = document.getElementById('add-goods-button');
const closeAddGoods = document.getElementById('close-goods-button');
const addGoodsBlock = document.getElementById('add-goods-manually-block');

const toggleAddGoodsBlock = () => {
  if (mainSection.style.display === 'block') {
    mainSection.style.display = 'none';
    addGoodsBlock.style.display = 'block';
  } else {
    mainSection.style.display = 'block';
    addGoodsBlock.style.display = 'none';
  }
};
const closeAddGoodsBlock = () => {
  mainSection.style.display = 'block';
  addGoodsBlock.style.display = 'none';
};
buttonAddGoods.addEventListener('click', toggleAddGoodsBlock);
closeAddGoods.addEventListener('click', closeAddGoodsBlock);
// photos upload
const fileInputs = document.querySelectorAll('.photos__input');

function handleFileLoad(event, index) {
  const imageElement = document.getElementById(`preview${index + 1}`);
  imageElement.src = event.target.result;
  imageElement.classList.remove('hidden');
  const iconElement = document.getElementById(`icon${index + 1}`);
  iconElement.style.display = 'none';
}

fileInputs.forEach((input, index) => {
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (event) {
        handleFileLoad(event, index);
      };
      reader.readAsDataURL(file);
    }
  });
});
// upload xsl file in excel blo
document.getElementById('file').addEventListener('change', function (event) {
  const fileLabelText = document.getElementById('file-label-text');
  const files = event.target.files;
  if (files.length > 0) {
    fileLabelText.textContent = `Selected file: ${files[0].name}`;
  } else {
    fileLabelText.textContent =
      'Нажмите, чтобы загрузить файл или перетащите файл в эту область';
  }
});
// add column
document.addEventListener('DOMContentLoaded', function () {
  const addButton = document.getElementById('column-button');
  const columnContainers = document.getElementsByClassName('column-container');

  if (columnContainers.length === 0) {
    console.error('No column containers found');
    return;
  }

  const columnContainer = columnContainers[0]; // Assuming you only have one container

  function createNewColumn(event) {
    event.preventDefault();
    const newColumn = columnContainer.firstElementChild.cloneNode(true);

    // Clear the input values in the cloned column
    const inputs = newColumn.querySelectorAll('input');
    inputs.forEach((input) => {
      input.value = '';
    });

    // Add the new column to the end of the container
    columnContainer.appendChild(newColumn);
  }

  addButton.addEventListener('click', createNewColumn);

  // Add event listener for delete buttons
  columnContainer.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-button')) {
      const column = event.target.closest('.column');

      if (columnContainer.children.length > 1) {
        column.remove();
      }
    }
  });
});

// delete
const columnContainer = document.getElementById('column-container');

columnContainer.addEventListener('click', function (event) {
  if (event.target.classList.contains('delete-button')) {
    const column = event.target.closest('.column');

    if (column !== columnContainer.querySelector('.column')) {
      column.remove();
    }
  }
});
