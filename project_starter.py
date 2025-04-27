import subprocess
import sys

# List of required modules
required_modules = [
    'Flask',
    'tensorflow',
    'nltk',
    'flask_cors',
    'numpy',
    'scikit-learn',
]

# Function to check if a module is installed
def is_module_installed(module):
    try:
        __import__(module)
        return True
    except ImportError:
        return False

# Check if each required module is installed
missing_modules = [module for module in required_modules if not is_module_installed(module)]

# If there are missing modules, install them
if missing_modules:
    print(f"Missing modules: {', '.join(missing_modules)}")
    print("Installing missing modules...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Now that the modules are ensured, run the Flask app
from spamClassifier import app  # assuming your app is in app.py

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
