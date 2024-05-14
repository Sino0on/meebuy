// avatar upload
const avatarInput = document.querySelector('#upload');
const avatar = document.querySelector('#avatar');

avatarInput.addEventListener('change', () => {
    const reader = new FileReader();
    reader.readAsDataURL(avatarInput.files[0]);
    reader.addEventListener('load', () => {
        avatar.src = reader.result;
        const formData = new FormData();
        // Добавляем файл в FormData под ключом 'avatar'
        formData.append('avatar', avatarInput.files[0]);

        const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
        console.log(csrftoken);
        // Отправляем запрос на сервер
        fetch('/change-avatar/', {
            method: 'POST',
            body: formData,
            credentials: 'include',  // Если требуется, чтобы cookies отправлялись с запросом
            headers: {
                'X-CSRFToken': csrftoken
            }
        }).then(response => {
            if (response.ok) {
                console.log('Avatar updated successfully');
                return response.json();
            } else {
                throw new Error('Something went wrong on API server!');
            }
        }).then(response => {
            console.log(response);
        }).catch(error => {
            console.error(error);
        });
    });
    console.log('tut');
})

// dropdown
const dropdownBtn = document.querySelector('.dropdown__btn');
const dropdownMenu = document.querySelector('.dropdown__menu');

dropdownBtn.addEventListener('click', () => {
    const isActive = dropdownMenu.classList.contains('active');
    dropdownMenu.style.maxHeight = isActive ? "0" : `${dropdownMenu.scrollHeight}px`;
    dropdownMenu.classList.toggle('active');
})

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