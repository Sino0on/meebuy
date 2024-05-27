const goods = document.getElementById("goods");
const category = document.getElementById("category");
const price = document.getElementById("price");
const autoloader = document.getElementById("autoload");
const excelLoader = document.getElementById("excel-loader");
const goodsBlock = document.getElementById("goods-block");
const categoryBlock = document.getElementById("category-block");
const priceBlock = document.getElementById("price-block");
const autoloaderBlock = document.getElementById("autoload-block");
const excelLoaderBlock = document.getElementById("excel-loader-block");

const toggleTab = (element) => {
  const tabs = [goods, category, price, autoloader, excelLoader];
  const blocks = [
    goodsBlock,
    categoryBlock,
    priceBlock,
    autoloaderBlock,
    excelLoaderBlock,
  ];
  for (let i = 0; i <= tabs.length; i++) {
    if (tabs[i] === element) {
      tabs[i].style.backgroundColor = "#FFFB98";
      blocks[i].style.display = "block";
    } else {
      tabs[i].style.backgroundColor = "";
      blocks[i].style.display = "none";
    }
  }
};

goods.addEventListener("click", () => toggleTab(goods));
category.addEventListener("click", () => toggleTab(category));
price.addEventListener("click", () => toggleTab(price));
autoloader.addEventListener("click", () => toggleTab(autoloader));
excelLoader.addEventListener("click", () => toggleTab(excelLoader));


//excel open block
const downloadExcel = document.getElementsByClassName("download-excel")[0]

const openExcelBlock = () => {
  if(goodsBlock.style.display === 'block'){
        goodsBlock.style.display = 'none'
    goods.style.backgroundColor = ''
     excelLoader.style.backgroundColor = "#FFFB98";
     excelLoaderBlock.style.display = "block";

  }else{
     excelLoader.style.display = "block";
    goods.style.backgroundColor = "#FFFB98";
    goodsBlock.style.display = 'none'
  }
}
downloadExcel.addEventListener("click", openExcelBlock)

// add category

const buttonAddCategory = document.getElementById("add-category");
const mainSection = document.getElementById("main-section");
const addCategoryBlock = document.getElementById("add-category-block");
const GoBackBtn = document.querySelector('#test222')

const toggleAddCategoryBlock = () => {
  if (mainSection.style.display === "block") {
    mainSection.style.display = "none";
    addCategoryBlock.style.display = "block";
  } else {
    mainSection.style.display = "block";
    addCategoryBlock.style.display = "none";
  }
};

buttonAddCategory.addEventListener("click", toggleAddCategoryBlock);
GoBackBtn.addEventListener('click', toggleAddCategoryBlock)
// add goods manually
const buttonAddGoods = document.getElementById("add-goods-button");
const closeAddGoods = document.getElementById("close-goods-button");
const addGoodsBlock = document.getElementById("add-goods-manually-block");

const toggleAddGoodsBlock = () => {
  if (mainSection.style.display === "block") {
    mainSection.style.display = "none";
    addGoodsBlock.style.display = "block";
  } else {
    mainSection.style.display = "block";
    addGoodsBlock.style.display = "none";
  }
};
const closeAddGoodsBlock = () => {
  mainSection.style.display = "block";
  addGoodsBlock.style.display = "none";
};
buttonAddGoods.addEventListener("click", toggleAddGoodsBlock);
closeAddGoods.addEventListener("click", closeAddGoodsBlock);

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
      reader.onload = function (event) {
        handleFileLoad(event, index);
      };
      reader.readAsDataURL(file);
    }
  });
});

// upload xsl file in excel block

// document.getElementById('file').addEventListener("change", function(event) {
//   const fileLabelText = document.getElementById('file-label-text');
//   const files = event.target.files;
//   if (files.length > 0) {
//     fileLabelText.textContent = `Selected file: ${files[0].name}`;
//
//     // Автоматически отправляем форму через 3 секунды
//     setTimeout(() => {
//       const formData = new FormData();
//       formData.append('file', files[0]);
//
//       fetch('http://localhost:8080', {
//         method: 'POST',
//         body: formData,
//       })
//       .then(response => response.text())
//       .then(data => {
//         console.log(data); // Обработка ответа сервера
//       })
//       .catch(error => {
//         console.error('Ошибка:', error);
//       });
//     }, 3000);
//   } else {
//     fileLabelText.textContent = 'Нажмите, чтобы загрузить файл или перетащите файл в эту область';
//   }
// });