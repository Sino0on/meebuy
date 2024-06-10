// burger menu
const burgerMenu = document.querySelector("#burgerMenu");
const burgerIcon = document.querySelector("#burgerIcon");
const closeIcon = document.querySelector("#closeIcon");
// search

const searchForm = document.querySelector("#searchForm");
const searchIcon = document.querySelector("#searchIconImg");

const toggleMenu = () => {
  if (burgerMenu.classList.contains("translate-x-0")) {
    burgerMenu.classList.remove("translate-x-0");
    burgerMenu.classList.add("translate-x-full");
  } else {
    burgerMenu.classList.add("translate-x-0");
    burgerMenu.classList.remove("translate-x-full");
  }
};

burgerIcon.addEventListener("click", toggleMenu);
closeIcon.addEventListener("click", toggleMenu);

// search

const toggleFormWidth = () => {
  searchForm.classList.toggle("w-3/4");
  searchForm.classList.toggle("w-min");
};

searchIcon.addEventListener("click", toggleFormWidth);

const auth_tabs = document.querySelectorAll(".auth_tab");

const toggleAuthTab = (clickedTab) => {
  auth_tabs.forEach((tab) => {
    if (tab === clickedTab) {
      tab.classList.add("tab_hover");
    } else {
      tab.classList.remove("tab_hover");
    }
  });
};

auth_tabs.forEach((tab) => {
  tab.addEventListener("click", () => toggleAuthTab(tab));
});

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("show-password")) {
    const passwordInput = event.target
      .closest(".flex")
      .querySelector(".password-input");
    const showPasswordIcon = event.target;
    const isPasswordVisible = passwordInput.getAttribute("type") === "text";

    if (isPasswordVisible) {
      passwordInput.setAttribute("type", "password");
      showPasswordIcon.setAttribute(
        "src",
        "/static/assets/images/icons/password-close.svg"
      );
    } else {
      passwordInput.setAttribute("type", "text");
      showPasswordIcon.setAttribute(
        "src",
        "/static/assets/images/icons/password-open.svg"
      );
    }
  }
});

const registerTab = document.getElementById("register-tab");
const loginTab = document.getElementById("login-tab");
const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const login = document.getElementById("login");
const register = document.getElementById("register");
const lastName = document.getElementById("name");
const number = document.getElementById("number");
const password = document.getElementById("password");
const passwordLog = document.getElementById("passwordLog");
const confirmAuth = document.getElementById("confirm");

const toggleTabRegister = () => {
  registerForm.style.maxHeight = `${registerForm.scrollHeight}px`;
  loginForm.style.maxHeight = "0px";
  lastName.classList.add("input-change");
  number.classList.add("password-an");
  password.classList.add("password-an");
  confirmAuth.classList.add("password-an");
  register.classList.add("register-an");
  registerTab.classList.add("tab-hover");
  loginTab.classList.remove("tab-hover");
  localStorage.setItem("activeTab", "register");

  registerForm.addEventListener(
    "animationend",
    () => {
      registerForm.classList.remove("input-change", "password-an");
      lastName.classList.remove("input-change");
      number.classList.remove("password-an");
      password.classList.remove("password-an");
      confirmAuth.classList.remove("password-an");
      register.classList.remove("register-an");
    },
    { once: true }
  );
};

const toggleTabLogin = () => {
  loginForm.style.maxHeight = `${loginForm.scrollHeight}px`;
  registerForm.style.maxHeight = "0px";
  login.classList.add("login-an");
  passwordLog.classList.add("password-an-log");
  loginTab.classList.add("tab-hover");
  registerTab.classList.remove("tab-hover");
  localStorage.setItem("activeTab", "login");

  loginForm.addEventListener(
    "animationend",
    () => {
      loginForm.classList.remove("login-an", "password-an-log", "login_img");
      passwordLog.classList.remove("password-an-log");
      login.classList.remove("login-an");
    },
    { once: true }
  );
};
const activeTab = localStorage.getItem("activeTab");

if (activeTab === "register") {
  toggleTabRegister();
} else if (activeTab === "login") {
  toggleTabLogin();
}

registerTab.addEventListener("click", toggleTabRegister);
loginTab.addEventListener("click", toggleTabLogin);

document.addEventListener("DOMContentLoaded", function () {
    if(loginForm.querySelector('.has-error')){
      console.log(loginForm.querySelector('.has-error'));
      loginTab.click();
    } else{
      registerTab.click();
    }
});