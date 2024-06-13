    const selectedItems = [];
const userId = document.getElementById("main").getAttribute('data-profile-id')
    const url = `${window.location.origin}/category/list/${userId}`; // Используем origin вместо host для включения протокола

console.log(userId)
// Отправляем запрос на сервер
fetch(url)
  .then(response => {
    if (response.ok) {
      return response.json(); // Разбираем JSON, если ответ успешный
    }
    throw new Error('Network response was not ok.'); // В случае ошибки в сетевом ответе
  })
  .then(data => {
    const treeArray = data; // Сохраняем данные в переменную

function createTree(treeArray, depth = 0) {
  const tree = document.createElement("ul");
  const plValue = Math.max(14 - 2 * depth, 4);
  tree.className = depth === 0 ? "" : `pl-${plValue}`;
  if (depth === 0) {
    tree.classList.add("divide-y", "divide-grey-light", "space-y-[15px]");
  }

  treeArray.forEach(item => {
    const li = document.createElement("li");
    li.className = "tree__item";
    console.log(item)

    const div = document.createElement("div");
    div.className = "cursor-pointer w-fit flex items-center gap-2.5 pt-[15px] text-dark-logo";

    const iconDiv = document.createElement("div");
    if (item.icon) {
      iconDiv.className = "flex justify-center items-center p-2.5 rounded-full bg-logo-color w-[37px] h-[37px] lg-md:w-12 lg-md:h-12";
      const img = document.createElement("img");
      img.src = item.icon;
      img.alt = `${item.title}`;
      iconDiv.appendChild(img);
    }

    const span = document.createElement("span");
    span.textContent = item.title;


    span.addEventListener("click", () => {
      if (!item.children || item.children.length === 0) {
        const index = selectedItems.indexOf(item.id);
        if (index === -1) {
          selectedItems.push(item.id);
          span.classList.add("active");
        } else {
          selectedItems.splice(index, 1);
          span.classList.remove("active");
        }
        updateSelectedItemsDisplay();
      }
    });

      if(item.is_selected){
      span.click();
    }

    const toggleIcon = document.createElement("img");
    toggleIcon.src = "/static/assets/images/icons/ios-arrow.svg";
    toggleIcon.alt = "Expand";
    toggleIcon.className = "toggle-icon transform transition-transform";

    div.appendChild(iconDiv);
    div.appendChild(span);
    if (item.children && item.children.length > 0) {
      div.appendChild(toggleIcon);
      div.addEventListener("click", function() {
        const nextUl = li.querySelector("ul");
        nextUl.classList.toggle("hidden");
        toggleIcon.classList.toggle("rotate-180");
      });
    }

    li.appendChild(div);

    if (item.children && item.children.length > 0) {
      const childUl = createTree(item.children, depth + 1);
      childUl.className += " hidden";
      li.appendChild(childUl);
    }

    tree.appendChild(li);
  });

  return tree;
}

document.getElementById("treeWrapper").appendChild(createTree(treeArray));
    console.log(treeArray); // Выводим данные в консоль для проверки
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error); // Обрабатываем возможные ошибки
  });



const categorySearch = document.getElementById("categorySearch");

categorySearch.addEventListener("input", () => {
  const value = categorySearch.value;
  const tree = document.getElementById("treeWrapper");
  const items = tree.querySelectorAll(".tree__item");
  items.forEach(item => {
    if (item.textContent.toLowerCase().includes(value.toLowerCase())) {
      item.style.display = "block";
    } else {
      item.style.display = "none";
    }
  });
});

function updateSelectedItemsDisplay() {
  console.log(selectedItems)
  document.getElementById("selectedCategory").value = selectedItems.join(", ");
}

const addNumberBtn = document.getElementById("addNumberBtn");
const numbersWrapper = document.querySelector(".numberInputs");

addNumberBtn?.addEventListener("click", () => {
  numbersWrapper.insertAdjacentHTML("beforeend", `
    <div class="flex justify-between items-center pr-7 relative">
      <input class="numbers" type="tel" name="phoneNumber" placeholder="+996 ХХХ ХХХ ХХХ">
      <img class="deletePhoneInput absolute top-[60%] right-0 -translate-y-1/2 cursor-pointer" src="/assets/images/icons/x.svg" alt="">
    </div>
  `);
});

numbersWrapper?.addEventListener("click", (event) => {
  if (event.target.classList.contains("deletePhoneInput")) {
    event.target.parentElement.remove();
  }
});


