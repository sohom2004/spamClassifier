import subprocess
import sys
import nltk
import requests
import zipfile
import io
import os

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
    
# Function to download and unzip WordNet data
def download_wordnet_data():
    nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data", "corpora")
    wordnet_zip_path = os.path.join(nltk_data_path, "wordnet.zip")
    
    # Check if WordNet is already downloaded
    if not os.path.exists(wordnet_zip_path):
        url = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("WordNet data download successful.")
            # Unzip the WordNet zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                os.makedirs(nltk_data_path, exist_ok=True)
                zip_ref.extractall(nltk_data_path)
            print("WordNet data extracted successfully.")
        else:
            print(f"Failed to download WordNet data. Status code: {response.status_code}")
    else:
        print("WordNet data already exists.")

# Download WordNet data if not already available
download_wordnet_data()

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
