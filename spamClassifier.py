from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from flask_cors import CORS
import re
import pickle

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes to allow API requests from different origins
CORS(app)

# Load the pre-trained GRU model for spam classification
model = load_model('best_gru_model.h5')

# Define the parameters for preprocessing that match what was used during model training
max_words = 5000  # Maximum number of words to consider in tokenization
max_len = 100     # Maximum length for padding sequences

# Load the tokenizer used during model training to preprocess incoming text messages
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Initialize lemmatizer from NLTK for reducing words to their base or root form
lemmatizer = WordNetLemmatizer()

# Function to preprocess input text (message) by:
# 1. Converting to lowercase
# 2. Removing non-alphanumeric characters
# 3. Tokenizing the text
# 4. Lemmatizing each word to its base form based on its part of speech
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove any non-alphanumeric characters
    words = word_tokenize(text)  # Tokenize the cleaned text into individual words
    pos_tags = pos_tag(words)  # Get the part-of-speech tags for each word

    # Lemmatize each word based on its POS tag (verb, noun, adjective, etc.)
    words = [lemmatizer.lemmatize(word, pos='v' if tag.startswith('V') else 
                                 ('n' if tag.startswith('NN') else 
                                  ('a' if tag.startswith('JJ') else 
                                   ('r' if tag.startswith('RB') else 'n'))))
            for word, tag in pos_tags]
    
    # Join the lemmatized words back into a single string and return
    return ' '.join(words)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page (frontend)

# Route for predicting whether the message is Spam or Ham
@app.route('/predict', methods=['POST'])
def predict():
    # Extract the message from the incoming JSON request
    data = request.get_json()
    message = data.get('message', '')

    # Preprocess the message (cleaning and lemmatization)
    clean_message = preprocess_text(message)

    # Tokenize the preprocessed message using the trained tokenizer
    sequence = tokenizer.texts_to_sequences([clean_message])

    # Pad the sequence to the same length as the model expects
    padded = pad_sequences(sequence, maxlen=max_len, padding='post', truncating='post')

    # Get the model's prediction (probability) on whether the message is Spam or Ham
    prediction = model.predict(padded)

    # Convert the predicted probability to a label ("Spam" or "Ham")
    label = "Spam" if prediction[0][0] > 0.5 else "Ham"

    # Return the prediction as a JSON response
    return jsonify({"label": label})

# Run the Flask app on port 5000 when executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
