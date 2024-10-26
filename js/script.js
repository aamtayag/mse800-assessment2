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
    history.replaceState(null, '', ''); // Remove the #login portion of the URL
}

function register() {
    alert('Redirecting to registration page...');
}
