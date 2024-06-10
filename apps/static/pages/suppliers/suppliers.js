
// tabs
function openTab(_, tabId) {
  const contents = document.querySelectorAll('.tab-content');
  contents.forEach(content => {
      content.style.display = 'none';
  });

  const allTabs = document.querySelectorAll('.tabs__item');
  allTabs.forEach(tab => {
      tab.classList.remove('active');
  });

  document.getElementById(tabId).style.display = 'block';
  const activeTab = Array.from(allTabs).find(tab => tab.onclick.toString().includes(`'${tabId}'`));
  if (activeTab) {
      activeTab.classList.add('active');
  }
}