const config = require('./config.json');
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios');
const { spawn } = require('child_process');

const app = express();
const PORT = config.NODE_PORT || 3000;
// const EMAIL_PORT = 5000;
const BACKEND_PORT = config.BACKEND_PORT || 2000;
const STATIC_SERVER_PORT = config.STATIC_SERVER_PORT || 8000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to SQLite database (or create it if it doesn't exist)
const db = new sqlite3.Database('TourBooking.db', (err) => {

    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the SQLite database.');
});

// Create a table if it doesn't exist
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, tour TEXT, name TEXT, email TEXT, date TEXT, status INT)");
});

// Start Python static server to serve index.html and static files
const pythonStaticServer = spawn('python', ['-m', 'http.server', STATIC_SERVER_PORT], { stdio: 'inherit' });

// start Python projcet
const pythonProcess = spawn('python', ['python/app.py'], { stdio: 'inherit' });
pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
});

pythonProcess.on('exit', (code) => {
    console.log(`Python process exited with code ${code}`);
});

// Route to insert data
app.post('/add-item', (req, res) => {
    const { tour, name, email, date, status } = req.body;

    const stmt = db.prepare("INSERT INTO bookings (tour, name, email, date, status) VALUES (?, ?, ?, ?, ?)");
    stmt.run(tour, name, email, date, status, function (err) {
        if (err) {
            return res.status(500).send('Error adding item: ' + err.message);
        }

        // Send email
        sendEmail(email, 'order_submission', name, this.lastID)
            .then(response => {
                console.log('Email sent successfully');
                res.status(201).send('Item added and email sent successfully with ID: ' + this.lastID);
            })
            .catch(error => {
                console.error('Error sending email:', error.message);
                res.status(201).send('Item added successfully but failed to send email with ID: ' + this.lastID);
            });

    });
    stmt.finalize();
});

// get config
app.get('/config', (req, res) => {
    res.json(config);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Function to send email
function sendEmail(recipient_email, email_type, email_name, order_id) {
    return axios.post(`http://localhost:${BACKEND_PORT}/send-email`, {
        recipient_email: recipient_email,
        email_type: email_type,
        email_name: email_name,
        order_id: order_id,
    });
}

