function openLoginForm() {
    const loginSection = document.getElementById('login');
    loginSection.style.display = 'block';

    // Use pushState to prevent the login page from being displayed when backing out
    history.pushState({ isLoginOpen: true }, '', '#login');

    window.onpopstate = (event) => {
        if (!event.state || !event.state.isLoginOpen) {
            closeLoginForm();
        }
    };
}

function closeLoginForm() {
    const loginSection = document.getElementById('login');
    loginSection.style.display = 'none';
    history.replaceState(null, '', ' '); // Remove the #login portion of the URL
}

function register() {
    alert('Redirecting to registration page...');
    // Implementing registration logic
}

// js/script.js
let currentLanguage = 'en'; // 默认语言为英语

// 语言切换函数
function switchLanguage() {
    const select = document.getElementById('language-select');
    currentLanguage = select.value; // 获取用户选择的语言
    updateContent(); // 调用更新内容的函数
}

// 更新页面内容的函数
function updateContent() {
    const translation = translations[currentLanguage];

   if (translation) {
        document.getElementById('main-title').innerText = translation.title;
        document.getElementById('nav-home').innerText = translation.nav.home;
        document.getElementById('nav-tours').innerText = translation.nav.tours;
        document.getElementById('nav-about').innerText = translation.nav.about;
        document.getElementById('nav-contact').innerText = translation.nav.contact;
        document.getElementById('nav-login').innerText = translation.nav.login;
        document.getElementById('section-title').innerText = translation.sectionTitle;
        document.getElementById('section-description').innerText = translation.description;
    }
}

// 确保在页面加载完成后执行
document.addEventListener('DOMContentLoaded', updateContent);