import { API_NODE_URL } from './config.js';
// Function to open the booking form modal
function openBookingForm(tourName, price) {
    const modal = document.getElementById("bookingFormModal");
    if (modal) {
        // Set the tour name in the form
        document.getElementById("tour-name").value = tourName;
        
        // Show the modal
        modal.style.display = "block";
        
        // Add event listener for outside click to close the modal
        window.onclick = function(event) {
            if (event.target === modal) {
                closeBookingForm();
            }
        };
    }
}

// Function to close the booking form modal
function closeBookingForm() {
    const modal = document.getElementById("bookingFormModal");
    if (modal) {
        modal.style.display = "none";
        window.onclick = null; // Remove outside click listener
    }
}

// Attach openBookingForm to "Book Now" button in tours section
document.querySelectorAll(".tour button").forEach(button => {
    button.addEventListener("click", function() {
        const tourName = this.parentElement.querySelector("h3").innerText;
        const price = this.parentElement.querySelector("strong").innerText; // Optional if needed
        openBookingForm(tourName, price);
    });
});


document.addEventListener('DOMContentLoaded', () => {
    // Function to open the booking form modal
    function openBookingForm(tourName, price) {
        const modal = document.getElementById("bookingFormModal");
        if (modal) {
            // Set the tour name in the form
            document.getElementById("tour-name").value = tourName;
            
            // Show the modal
            modal.style.display = "block";
            
            // Add event listener for outside click to close the modal
            window.onclick = function(event) {
                if (event.target === modal) {
                    closeBookingForm();
                }
            };
        } else {
            console.error("Booking form modal not found.");
        }
    }

    // Function to close the booking form modal
    function closeBookingForm() {
        const modal = document.getElementById("bookingFormModal");
        if (modal) {
            modal.style.display = "none";
            window.onclick = null; // Remove outside click listener
        }
    }

    // Attach openBookingForm to each "Book Now" button in the tours section
    document.querySelectorAll(".tour button").forEach(button => {
        button.addEventListener("click", function() {
            const tourName = this.parentElement.querySelector("h3").innerText;
            const price = this.parentElement.querySelector("strong").innerText; // Optional if needed
            openBookingForm(tourName, price);
        });
    });

    // Attach openBookingForm to "Booking Tour" button in Manage Booking modal
    const manageBookingButton = document.querySelector('#manageBookingModal .button-container button');
    if (manageBookingButton) {
        manageBookingButton.addEventListener("click", function() {
            openBookingForm("Example Tour", 100);
        });
    } else {
        console.error("Manage Booking 'Booking Tour' button not found.");
    }
});

// Attach event listener to form submit
document.getElementById("tourForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const tour = document.getElementById("tour-name").value;
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const date = document.getElementById("date").value;
    const status = "Pending"; // Default status

    // Create a request payload
    const payload = {
        tour: tour,
        name: name,
        email: email,
        date: date,
        status: status
    };

    try {
        // Send booking request to the backend
	const response = await fetch(`${API_NODE_URL}/add-item`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        // Handle response from the server
        if (response.ok) {
            const result = await response.text();
            alert("Booking submitted successfully: " + result);
            // Redirect to homepage after alert
            window.location.href = "index.html"; // Replace with the actual path of your homepage
        } else {
            const error = await response.text();
            alert("Booking failed: " + error);
        }
    } catch (error) {
        console.error("Error submitting booking:", error);
        alert("An error occurred. Please try again later.");
    }
});
