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
			console.log('no valid role:', role);
            return 0; // 0 means no valid role found
    }
}

// Function to convert role
function convertRole(roleId) {
    switch(roleId) {
        case '1':
            return 'Admin';
        case '2':
            return 'User';
        case '3':
            return 'Customer';
        default:
            return 'Unknown';
    }
}

// Function to handle login
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'admin123') { // Simple hardcoded authentication
        document.getElementById('login-section').style.display = 'none';
        document.querySelector('header').style.display = 'block';
        document.getElementById('admin-home').style.display = 'block';
        document.querySelector('footer').style.display = 'block';
    } else {
        alert('Invalid username or password');
    }
});

// Event listeners for navigation
document.getElementById('nav-manage-users').addEventListener('click', () => {
    document.getElementById('admin-home').style.display = 'none';
    document.getElementById('manage-users').style.display = 'block';
    document.getElementById('manage-tours').style.display = 'none';
    loadUsers();
});

document.getElementById('nav-manage-tours').addEventListener('click', () => {
    document.getElementById('admin-home').style.display = 'none';
    document.getElementById('manage-users').style.display = 'none';
    document.getElementById('manage-tours').style.display = 'block';
    loadTours();
});


// Add event listener for form submission
document.getElementById('user-form').addEventListener('submit', async function(event) {
    event.preventDefault();
	const logined_username = "admin";
    const new_username = document.getElementById('new-username').value;
	const password = document.getElementById('new-password').value;
    const new_user_email = document.getElementById('new-email').value;
    const selectedRole = document.getElementById('new-role').value;
	
	const roles = roleMapping(selectedRole);
	
	const requestBody = {
        logined_username,
        new_user_email,
        new_username,
        password,
        roles
    };

    // Send new user data to the backend
    const response = await fetch(`${API_BASE_URL}/admin-create-users`, {
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

// Function to fetch and display users
async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin-query-userlist?logined_username=admin`);
        if (response.ok) {
            const users = await response.json();
            const userTableBody = document.querySelector('#user-table tbody');
            userTableBody.innerHTML = ''; // Clear existing content
            let index = 1;
            // Access userlist inside the response
            users.userlist.forEach(user => {
                const row = document.createElement('tr');
                const roleName = convertRole(user.roles);
                row.innerHTML = `
                    <td>${index}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>                                
                    <td>${roleName}</td>
                    <td>
                        <button class="table-actions" onclick="openRoleSelectionModal('${user.username}', '${user.email}')">ModifyRoles</button>
                    </td>
                `;
                userTableBody.appendChild(row);
                index++;
            });
        } else {
            alert('Failed to load users. Status code: ' + response.status);
        }
    } catch (error) {
        console.error('Error fetching users:', error);
        alert('An error occurred while loading users.');
    }
}


// Create a modal dynamically
function openRoleSelectionModal(username, email) {
    // Create a simple modal for role selection
    const modal = document.createElement('div');
    modal.id = 'role-modal';
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'white';
    modal.style.padding = '20px';
    modal.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.2)';
    modal.style.zIndex = '1000';

    // Modal content: select for roles and buttons
    modal.innerHTML = `
        <h2>Modify Role for ${username} (${email})</h2>
        <label for="role-select">Select a new role:</label>
        <select id="role-select">
            <option value="admin">Admin</option>
            <option value="user">User</option>
            <option value="customer">Customer</option>
        </select><br><br>
        <button id="confirm-role-btn">Confirm</button>
        <button id="cancel-role-btn">Cancel</button>
    `;

    // Append modal to body
    document.body.appendChild(modal);

    // Add event listeners for buttons
    document.getElementById('confirm-role-btn').addEventListener('click', function() {
        const selectedRole = document.getElementById('role-select').value;
        modifyUserRoles(username, email, selectedRole);
        document.body.removeChild(modal);  // Remove modal after selection
    });

    document.getElementById('cancel-role-btn').addEventListener('click', function() {
        document.body.removeChild(modal);  // Close modal without action
    });
}



// Function to modify user roles
async function modifyUserRoles(username, email, newRole) {

    const logined_username = "admin";  // Hardcoded for now, could be dynamic
    const roles = roleMapping(newRole);  // Convert role to internal ID or format

    const requestBody = {
        logined_username,
        email,
        username,
        roles
    };

    try {
        const response = await fetch(`${API_BASE_URL}/admin-modify-user-roles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (response.ok) {
            alert('User role updated successfully!');
            loadUsers();  // Reload the user list
        } else {
            alert('Failed to update user role.');
        }
    } catch (error) {
        console.error('Error updating user role:', error);
        alert('An error occurred while updating the user role.');
    }
}


// Function to fetch and display tours
async function loadTours() {
    const response = await fetch(`${API_BASE_URL}/get-tours`);
    if (response.ok) {
        const tours = await response.json();
        const tourTableBody = document.querySelector('#tour-table tbody');
        tourTableBody.innerHTML = '';
        tours.forEach(tour => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${tour.id}</td>
                <td>${tour.name}</td>
                <td>${tour.price}</td>
                <td>${tour.duration}</td>
                <td>
                    <button onclick="editTour(${tour.id})">Edit</button>
                    <button onclick="deleteTour(${tour.id})">Delete</button>
                </td>
            `;
            tourTableBody.appendChild(row);
        });
    } else {
        alert('Failed to load tours');
    }
}

// Placeholder functions for editing and deleting tours
function editTour(tourId) {
    alert('Edit tour functionality for tour ID: ' + tourId);
}

function deleteTour(tourId) {
    alert('Delete tour functionality for tour ID: ' + tourId);
}




// Expose the function to the global scope
window.openRoleSelectionModal = openRoleSelectionModal;
window.modifyUserRoles = modifyUserRoles;
window.editTour = editTour;
window.deleteTour = deleteTour;
