
# mse800-assessment2
MSE800 Assessment 2

## Step 1: Set Up Your Environment

### 1. Install Node.js
If you haven't already, download and install Node.js from the [Node.js official website](https://nodejs.org). Node.js comes with npm (Node Package Manager), which is required to install the necessary packages for this project.

### 2. Install Python
Ensure Python is installed on your system, as it’s required for running the static server and additional scripts in this project.

- **Windows**: Download and install Python from the [official website](https://www.python.org/downloads/). During installation, make sure to check the option "Add Python to PATH."
- **macOS**: Python 2.x may come pre-installed. To install Python 3, use Homebrew:
  ```bash
  brew install python
  ```
- **Linux**: Python may be pre-installed on most distributions. If not, you can install it using your package manager:
  ```bash
  sudo apt-get install python3
  ```

After installing Python, confirm it’s accessible by running:
```bash
python --version
```

### 3. Install SQLite3
SQLite3 is the database used in this project.

- **macOS**: Install SQLite3 using Homebrew. If you don’t have Homebrew, install it from [brew.sh](https://brew.sh). Then run:
  ```bash
  brew install sqlite3
  ```
  
- **Windows and Linux**: Download the appropriate version of SQLite3 from the [SQLite website](https://sqlite.org/download.html) or install it using your package manager.

### 4. Create a Project Directory
Create a directory for your project and navigate into it:
```bash
mkdir tour-booking-system
cd tour-booking-system
```

### 5. Initialize a Node.js Project
Initialize a new Node.js project, which will generate a `package.json` file:
```bash
npm init -y
```

### 6. Install Required Packages
Install the necessary packages for the project:
```bash
npm install express sqlite3 body-parser cors axios
```

## Step 2: Running the Project

1. **Start the Express Server**
   Run the main server file (assuming it's `server.js`) to start the application:
   ```bash
   node server.js
   ```

   **Note**: If you encounter errors with SQLite3, try rebuilding it with the following command:
   ```bash
   npm rebuild sqlite3
   ```

2. **Python Static Server and Back-End Service**
   The project also includes a Python static server and a back-end service component:
   - Ensure `app.py` is in the `python` folder within your project directory.
   - The static server and back-end service will start automatically when you run the Express server.

## Port Configuration

The server address information is configured in two separate files:

1. **Back-End Configuration**: Modify the `config.json` file for back-end services.

   - **Default Ports**:
     - `2000` for the Python back-end service.
     - `3000` for the Node.js back-end service.
     - `8000` for the Python static server.

   - **File Path**: `config.json` should be located in the project root directory.

   - **File Contents**:
     ```json
     {
         "NODE_PORT": 3000,
         "BACKEND_PORT": 2000,
         "STATIC_SERVER_PORT": 8000
     }
     ```

2. **Front-End Configuration**: Modify the `js/config.js` file to specify API base URLs for front-end requests.

   - **File Contents**:
     ```javascript
     // Base Host Python service
     const API_BASE_URL = 'http://localhost:2000';

     // Base Host Node service
     const API_NODE_URL = 'http://localhost:3000';

     export { API_BASE_URL, API_NODE_URL };
     ```

   **Note**: If you modify the ports in `config.json`, ensure the corresponding API URLs in `js/config.js` are also updated to match.

### Additional Information
- **Database**: The project uses an SQLite database named `TourBooking.db`, which will be created in the project directory if it doesn’t already exist. This database stores booking information.
- **API Endpoints**:
  - `POST /add-item`: Adds a booking item to the database. This also triggers an email notification.
  
### Troubleshooting
If you encounter issues:
- Ensure all dependencies are installed with `npm install`.
- Verify that Python is correctly set up and accessible through the command line.
- Confirm that the `TourBooking.db` file is created in the project directory.
