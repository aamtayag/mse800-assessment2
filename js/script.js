// Function to open the login form
function openLoginForm() {
    const loginSection = document.getElementById('login');
    loginSection.style.display = 'block';
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
}

// Default language is English
let currentLanguage = 'en';

async function loadTranslations(language) {
    try {
        const response = await fetch('/languages/' + language + '.json');
        if (!response.ok) {
            throw new Error('Failed to load translation file');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

function updateContent(translations) {
    document.querySelectorAll('[data-lang-key]').forEach(el => {
        const key = el.getAttribute('data-lang-key');
        const text = key.split('.').reduce((o, i) => (o && o[i] !== undefined) ? o[i] : null, translations);
        if (text) el.innerText = text;
    });
}

async function switchLanguage() {
    const select = document.getElementById('language-select');
    currentLanguage = select.value; // Get selected language
    localStorage.setItem('language', currentLanguage); // Save to localStorage
    const translations = await loadTranslations(currentLanguage);
    if (translations) {
        updateContent(translations);
    }
}

// Function to load the language select component dynamically
function loadLanguageSelect() {
    fetch('/pages/language-select.html')  // Adjust the path accordingly
        .then(response => response.text())
        .then(html => {
            // Create a container and append the loaded HTML
            const languageSelectContainer = document.createElement('div');
            languageSelectContainer.innerHTML = html;
            document.body.appendChild(languageSelectContainer); // Append it to the body

            // Now that the select has been loaded, trigger switchLanguage to set it up
            const savedLanguage = localStorage.getItem('language') || 'en';
            document.getElementById('language-select').value = savedLanguage;
            currentLanguage = savedLanguage;
            switchLanguage(); // Apply the saved language translations
        });
}

// Load the language select and the translations on page load
document.addEventListener('DOMContentLoaded', () => {
    loadLanguageSelect();  // Load the language selector component dynamically
});
