from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import easyocr
from googletrans import Translator
from PIL import Image
import pandas as pd
from fuzzywuzzy import fuzz
import spacy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Load your IPC dataset
ipc_dataset_path = '/home/om/Desktop/REPOS/RJPOLICE_HACK_191_ProblemStatement_4/FIR_DATASET.csv'
ipc_dataset = pd.read_csv(ipc_dataset_path)

# Load spaCy English model
nlp = spacy.load("en_core_web_md")

# Function to detect text using EasyOCR
def detect_text_with_easyocr(image_path, language='hi'):
    reader = easyocr.Reader([language])
    result = reader.readtext(image_path)
    return result

# Function to translate text from Hindi to English
def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to match the English text with IPC sections using spaCy and fuzzy matching
def match_ipc_section(english_text, ipc_dataset):
    # Initialize variables for best match and score
    best_match = None
    best_score = 0

    # Iterate through dataset entries
    for index, row in ipc_dataset.iterrows():
        # Extract the description from the dataset
        description = str(row['Description'])

        # Calculate the semantic similarity score using spaCy
        semantic_score = nlp(english_text).similarity(nlp(description))

        # Calculate the fuzzy match score
        fuzzy_score = fuzz.ratio(english_text, description)

        # Combine scores to get an overall score
        overall_score = (semantic_score + fuzzy_score) / 2

        # Update best match if the current score is higher
        if overall_score > best_score:
            best_score = overall_score
            best_match = row

    return best_match, best_score

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Use EasyOCR to detect and read text in Hindi
            text_results = detect_text_with_easyocr(file_path, language='hi')

            # Extract the text from the results
            hindi_text = ' '.join(result[1] for result in text_results)

            # Translate the Hindi text to English
            english_text = translate_text(hindi_text, target_language='en')

            # Match the text with IPC sections using spaCy and fuzzy matching
            matched_section, match_score = match_ipc_section(english_text, ipc_dataset)

            return render_template('index.html', image_path=file_path, hindi_text=hindi_text,
                                   english_text=english_text, matched_section=matched_section, match_score=match_score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
