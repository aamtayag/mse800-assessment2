import { API_BASE_URL } from './config.js';
// Attach event listener to form submit
document.getElementById("cancelForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const bookingId = document.getElementById("bookingId").value;
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const reason = document.getElementById("reason").value;
    const comments = document.getElementById("comments").value;

    // Create a request payload
    const payload = {
        id: bookingId,
        name: name,
        email: email,
		
		// not use
        reason: reason,
        comments: comments
    };

    try {
        // Send cancellation request to the backend
        const response = await fetch(`${API_BASE_URL}/booking-cancellation`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        // Handle response from the server
        if (response.ok) {
            const result = await response.json();
            alert("Cancellation submitted successfully: " + result.message);
            // Redirect to homepage after alert
			window.location.href = "../index.html";
        } else {
            const error = await response.json();
            alert("Cancellation failed: " + error.message);
        }
    } catch (error) {
        console.error("Error submitting cancellation:", error);
        alert("An error occurred. Please try again later.");
    }
});
