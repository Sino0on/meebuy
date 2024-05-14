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

// add category

const buttonAddCategory = document.getElementById("add-category");
const mainSection = document.getElementById("main-section");
const addCategoryBlock = document.getElementById("add-category-block");

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
