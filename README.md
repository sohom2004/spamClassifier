# Spam Detection (plus web app)

This project is a Spam Message Detection web application built using Flask for the backend and HTML for the frontend.
It allows users to input a message and classify it as Spam or Ham (Not Spam).

# Features
- Real-time spam detection
- Simple and clean web interface
- Easy project setup via launcher.bat
- Manual setup option available

# Requirements
- Python 3.x
- pip (Python package manager)
- Internet connection (for first-time dependency installation)

# Setup and Usage
## Option 1: Easy Launch (Recommended)
Use the provided launcher.bat file to automatically install dependencies and start the server.

Steps:
- Download or clone the project.
- Double-click launcher.bat. (launcher.bat will install missing dependencies automatically)
- Your default browser should open at http://127.0.0.1:5000/.
- Start using the app!

## Option 2: Manual Setup
If you prefer manual control, follow these steps:

1. Install dependencies
Open a terminal (or command prompt) in the project directory and run:
```bash
pip install -r requirements.txt
```

2. Start the Flask server
Run the following command:
```bash
python spamClassifier.py
```

3. Open your browser
Visit: http://127.0.0.1:5000/
Start entering messages to detect spam!

# Notes
- Make sure Python is added to your system PATH.
- The launcher.bat file handles everything automatically for you, including missing dependencies.
