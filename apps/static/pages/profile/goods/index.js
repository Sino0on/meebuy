const goods = document.getElementById("goods");
const category = document.getElementById("category");
const price = document.getElementById("price");
const excelLoader = document.getElementById("excel-loader");
const goodsBlock = document.getElementById("goods-block");
const categoryBlock = document.getElementById("category-block");
const priceBlock = document.getElementById("price-block");
const excelLoaderBlock = document.getElementById("excel-loader-block");

const toggleTab = (element) => {
  // if (element) {
  const tabs = [goods, category, price, excelLoader];
  const blocks = [goodsBlock, categoryBlock, priceBlock, excelLoaderBlock];
  for (let i = 0; i <= tabs.length; i++) {
    if (tabs[i] === element) {
      tabs[i].style.backgroundColor = "#FFFB98";
      blocks[i].style.display = "block";
      // return;
    } else {
      tabs[i].style.backgroundColor ? (tabs[i].style.backgroundColor = "") : "";
      blocks[i].style.display = "none";
    }
  }
  // }
};
goods.addEventListener("click", () => toggleTab(goods));
category.addEventListener("click", () => toggleTab(category));
price.addEventListener("click", () => toggleTab(price));
excelLoader.addEventListener("click", () => toggleTab(excelLoader));

// go to upload excel block from goods

const buttonToExcel = document.querySelectorAll(".download-excel");

const toggleGoUploadExcelBlock = () => {
  toggleTab(excelLoader);
};

buttonToExcel.forEach((button) => {
  button.addEventListener("click", toggleGoUploadExcelBlock);
});

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
      const reader = new FileReader();
      reader.onload = function (event) {
        handleFileLoad(event, index);
      };
      reader.readAsDataURL(file);
    }
  });
});
// upload xsl file in excel blo
document.getElementById("file").addEventListener("change", function (event) {
  const fileLabelText = document.getElementById("file-label-text");
  const files = event.target.files;
  if (files.length > 0) {
    fileLabelText.textContent = `Selected file: ${files[0].name}`;
  } else {
    fileLabelText.textContent =
      "Нажмите, чтобы загрузить файл или перетащите файл в эту область";
  }
});
// add column
const testDiv = document.querySelector(".test");
document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("column-button");
  const columnContainers = document.querySelectorAll(".column-container");

  if (columnContainers.length === 0) {
    console.error("No column containers found");
    return;
  }

  function createNewColumn(e) {
    e.preventDefault();
    const newColumnHTML = `
              <div
                class="column-container flex flex-col gap-5"
                >
                <div
                    class="column sm:p-9 p-5 box-shadow flex flex-col lg-md:gap-7 gap-10 m-0"
                  >
                  <div class="grid md:grid-cols-3 gap-5">
                      <div class="flex flex-col gap-1">
                        <h6
                          class="text-[#2B292C] font-semibold text-[18px]"
                        >
                          Название колонки
                        </h6>
                        <p
                          class="text-[#2B292C] font-light text-[16px] pb-4"
                        >
                          Например: Мелкий опт
                        </p>
                        <input
                          class="bg-[#F9F9F9] border border-[#E6E6E6] py-3 pl-5 rounded-2xl"
                          type="text" value="" name="name"
                        />
                      </div>
                      <div class="flex flex-col gap-1">
                        <h6
                          class="text-[#2B292C] font-semibold text-[18px]"
                        >
                          Формула расчета
                        </h6>
                        <p
                          class="text-[#2B292C] font-light text-[16px] pb-4"
                        >
                          Например: +50%
                        </p>
                        <input
                          class="bg-[#F9F9F9] border border-[#E6E6E6] py-3 pl-5 rounded-2xl"
                          type="text" value="" name="formula"
                        />
                      </div>
                      <div class="flex flex-col gap-1">
                        <h6
                          class="text-[#2B292C] font-semibold text-[18px]"
                        >
                          Сумма от
                        </h6>
                        <p
                          class="text-[#2B292C] font-light text-[16px] pb-4"
                        >
                          0 - от любой суммы
                        </p>
                        <input
                          class="bg-[#F9F9F9] border border-[#E6E6E6] py-3 pl-5 rounded-2xl"
                          type="text" value="" name="min_order_amount"
                        />
                      </div>
                    </div>
                    <div
                      class="delete-button flex items-center gap-3 cursor-pointer text-[#A0A0A0] text-[16px] font-light font-mulish"
                    >
                      <svg
                        width="20"
                        height="21"
                        viewBox="0 0 20 21"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M8 4H12C12 3.46957 11.7893 2.96086 11.4142 2.58579C11.0391 2.21071 10.5304 2 10 2C9.46957 2 8.96086 2.21071 8.58579 2.58579C8.21071 2.96086 8 3.46957 8 4ZM6.5 4C6.5 3.54037 6.59053 3.08525 6.76642 2.66061C6.94231 2.23597 7.20012 1.85013 7.52513 1.52513C7.85013 1.20012 8.23597 0.942313 8.66061 0.766422C9.08525 0.59053 9.54037 0.5 10 0.5C10.4596 0.5 10.9148 0.59053 11.3394 0.766422C11.764 0.942313 12.1499 1.20012 12.4749 1.52513C12.7999 1.85013 13.0577 2.23597 13.2336 2.66061C13.4095 3.08525 13.5 3.54037 13.5 4H19.25C19.4489 4 19.6397 4.07902 19.7803 4.21967C19.921 4.36032 20 4.55109 20 4.75C20 4.94891 19.921 5.13968 19.7803 5.28033C19.6397 5.42098 19.4489 5.5 19.25 5.5H17.93L16.76 17.611C16.6702 18.539 16.238 19.4002 15.5477 20.0268C14.8573 20.6534 13.9583 21.0004 13.026 21H6.974C6.04186 21.0001 5.1431 20.653 4.45295 20.0265C3.7628 19.3999 3.33073 18.5388 3.241 17.611L2.07 5.5H0.75C0.551088 5.5 0.360322 5.42098 0.21967 5.28033C0.0790175 5.13968 0 4.94891 0 4.75C0 4.55109 0.0790175 4.36032 0.21967 4.21967C0.360322 4.07902 0.551088 4 0.75 4H6.5ZM8.5 8.75C8.5 8.55109 8.42098 8.36032 8.28033 8.21967C8.13968 8.07902 7.94891 8 7.75 8C7.55109 8 7.36032 8.07902 7.21967 8.21967C7.07902 8.36032 7 8.55109 7 8.75V16.25C7 16.4489 7.07902 16.6397 7.21967 16.7803C7.36032 16.921 7.55109 17 7.75 17C7.94891 17 8.13968 16.921 8.28033 16.7803C8.42098 16.6397 8.5 16.4489 8.5 16.25V8.75ZM12.25 8C12.4489 8 12.6397 8.07902 12.7803 8.21967C12.921 8.36032 13 8.55109 13 8.75V16.25C13 16.4489 12.921 16.6397 12.7803 16.7803C12.6397 16.921 12.4489 17 12.25 17C12.0511 17 11.8603 16.921 11.7197 16.7803C11.579 16.6397 11.5 16.4489 11.5 16.25V8.75C11.5 8.55109 11.579 8.36032 11.7197 8.21967C11.8603 8.07902 12.0511 8 12.25 8ZM4.734 17.467C4.78794 18.0236 5.04724 18.5403 5.46137 18.9161C5.87549 19.292 6.41475 19.5001 6.974 19.5H13.026C13.5853 19.5001 14.1245 19.292 14.5386 18.9161C14.9528 18.5403 15.2121 18.0236 15.266 17.467L16.424 5.5H3.576L4.734 17.467Z"
                          fill="#A0A0A0"
                        />
                      </svg>

                      <p class="delete-button">Удалить колонку</p>
                    </div>
                </div>
            </div>
    `;

    const tempContainer = document.createElement("div");
    tempContainer.innerHTML = newColumnHTML.trim();
    const newColumn = tempContainer.firstChild;

    testDiv.appendChild(newColumn);
  }

  addButton.addEventListener("click", (e) => createNewColumn(e));

  columnContainers.forEach((content) => {
    content.addEventListener("click", function (event) {
      if (event.target.classList.contains("delete-button")) {
        const column = event.target.closest(".column");

        if (columnContainers.length >= 1) {
          column.remove();
        }
      }
    });
  });
});
