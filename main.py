from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import os

app = FastAPI()

# Load the pre-trained SVM classifier and TF-IDF vectorizer
classifier = load('svm_classifier.joblib')
vectorizer = load('tfidf_vectorizer.joblib')

# Load the label encoder used during training
label_encoder = load('label_encoder.joblib')

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
    # Lowercasing
    text = text.lower()
    # Tokenization
    tokens = nltk.word_tokenize(text)
    # Remove stopwords
    german_stop_words = set(stopwords.words('german'))
    filtered_tokens = [token for token in tokens if token not in german_stop_words]
    preprocessed_text = ' '.join(filtered_tokens)
    return preprocessed_text

def predict_label(text):
    preprocessed_text = preprocess(text)
    text_vectorized = vectorizer.transform([preprocessed_text])
    prediction = classifier.predict(text_vectorized)
    return prediction[0]

def validate_german(text):
    # Define valid German characters including umlauts and spaces
    valid_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöüÄÖÜß ")

    # Check if all characters in the text are valid German characters or spaces
    for char in text:
        if char not in valid_characters:
            return False
    return True

def contains_number_or_email(text):
    # Check if the text contains any numbers or email patterns
    if any(re.findall(r'\d+|[\w\.-]+@[\w\.-]+', text)):
        return True
    return False

@app.get("/", response_class=HTMLResponse)
async def home():
    # HTML form for text input
    html_content = """
    <html>
    <head>
        <title>Text Classification</title>
    </head>
    <body>
        <h1>Text Prediction</h1>
        <form action="/predict/" method="post">
            <label for="text">Enter text (German only, no numbers or emails):</label><br>
            <input type="text" id="text" name="text" pattern="[A-Za-zßüÜäÄöÖ\s]+" required><br>
            <input type="submit" value="Predict">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/predict/")
async def predict_text(text: str = Form(...)):
    # Check if the entered text is in German and does not contain numbers or emails
    if not validate_german(text):
        raise HTTPException(status_code=400, detail="Please enter text in German only, without numbers or emails.")
    # Get prediction for the input text
    prediction = predict_label(text)
    # Inverse transform the predicted label to get the actual label
    actual_label = label_encoder.inverse_transform([prediction])[0]
    return {"prediction": actual_label}
port = os.environ.get('PORT', 8000)  # Default to port 8000 if PORT environment variable is not set
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)