// admin.js
import { API_BASE_URL } from './config.js';
// Show modal for adding new user
document.getElementById('add-user-btn').addEventListener('click', () => {
    document.getElementById('user-modal').style.display = 'flex'; // Show modal
});

// Close modal when the "Close" button is clicked
document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('user-modal').style.display = 'none'; // Hide modal
});

// Function to map role names to numbers
function roleMapping(role) {
    switch (role) {
        case 'admin':
            return 1;
        case 'user':
            return 2;
        case 'customer':
            return 3;
        default:
            return 0; // 0 means no valid role found
    }
}

// Add event listener for form submission
document.getElementById('user-form').addEventListener('submit', async function(event) {
    event.preventDefault();
	const logined_username = "admin";
    const new_username = document.getElementById('new-username').value;
	const password = document.getElementById('new-password').value;
    const new_user_email = document.getElementById('new-email').value;
    const selectedRole = document.getElementById('new-role').value;
	
	const roles = roleMapping[selectedRole];
	
	const requestBody = {
        logined_username,
        new_user_email,
        new_username,
        password,
        roles
    };

    // Send new user data to the backend
    const response = await fetch(`${API_BASE_URL}/add-user`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
    });

    if (response.ok) {
        alert('New user added successfully!');
        document.getElementById('user-modal').style.display = 'none';
        loadUsers(); // Reload the user list
    } else {
        alert('Failed to add user');
    }
});

