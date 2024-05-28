// Mobile tab menu
document.addEventListener("DOMContentLoaded", () => {
  const tabs = [
    {
      menuTab: document.getElementById("menu-home"),
      activeIcon: document.getElementById("home-active"),
      noneActiveIcon: document.getElementById("home-none-active"),
    },
    {
      menuTab: document.getElementById("menu-messages"),
      activeIcon: document.getElementById("messages-active"),
      noneActiveIcon: document.getElementById("messages-none-active"),
    },
    {
      menuTab: document.getElementById("menu-procurement"),
      activeIcon: document.getElementById("procurement-active"),
      noneActiveIcon: document.getElementById("procurement-none-active"),
    },
    {
      menuTab: document.getElementById("menu-profile"),
      activeIcon: document.getElementById("profile-active"),
      noneActiveIcon: document.getElementById("profile-none-active"),
    },
  ];

  const currentPath = window.location.pathname;

  // Function to set active tab
  const setActiveTab = (currentPath) => {
    tabs.forEach((tab) => {
      if (currentPath === tab.menuTab.getAttribute("href")) {
        tab.activeIcon.style.display = "block";
        tab.noneActiveIcon.style.display = "none";
      } else {
        tab.activeIcon.style.display = "none";
        tab.noneActiveIcon.style.display = "block";
      }
    });
  };

  // Initialize active tab on page load
  setActiveTab(currentPath);

  // Add event listeners to each tab for click navigation
  tabs.forEach((tab) => {
    tab.menuTab.addEventListener("click", (event) => {
      event.preventDefault();
      window.location.href = tab.menuTab.getAttribute("href");
      setActiveTab(tab.menuTab.getAttribute("href"));
    });
  });
});
