from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from flask_cors import CORS
import re
import pickle

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the trained GRU model
model = load_model('best_gru_model.h5')

# Parameters (must match what was used during training)
max_words = 5000
max_len = 100

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = word_tokenize(text)
    pos_tags = pos_tag(words)  
    words = [lemmatizer.lemmatize(word, pos='v' if tag.startswith('V') else 
                                 ('n' if tag.startswith('NN') else 
                                  ('a' if tag.startswith('JJ') else 
                                   ('r' if tag.startswith('RB') else 'n'))))
            for word, tag in pos_tags]
    return ' '.join(words)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get('message', '')

    # Preprocess the message
    clean_message = preprocess_text(message)

    # Tokenize and pad
    sequence = tokenizer.texts_to_sequences([clean_message])
    padded = pad_sequences(sequence, maxlen=max_len, padding='post', truncating='post')

    # Predict
    prediction = model.predict(padded)

    # Convert probability to label
    label = "Spam" if prediction[0][0] > 0.5 else "Ham"

    return jsonify({"label": label})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)