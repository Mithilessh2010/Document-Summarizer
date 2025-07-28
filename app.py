"""
Document Summarizer Web App
===========================

This Flask application allows users to upload or paste text from various document types
(.txt, .pdf, .docx, .md, .html, .csv) and generate AI-based summaries using the Hugging Face Transformers library.

Dependencies:
- Flask: Web framework
- Transformers: Summarization model
- Torch: Backend for transformers
- python-docx: For reading .docx files
- PyPDF2: For reading .pdf files
- BeautifulSoup4: For .html parsing
- chardet: For encoding detection
- pandas: For .csv parsing
"""

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from transformers import pipeline
import docx
import PyPDF2
import pandas as pd
from bs4 import BeautifulSoup
import chardet

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the summarization pipeline from Hugging Face
summarizer = pipeline("summarization")

# Function to extract text from various document types
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == '.txt':
            # Detect encoding and read file
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding']
                text = raw_data.decode(encoding)

        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

        elif ext == '.docx':
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif ext == '.csv':
            df = pd.read_csv(file_path)
            text = df.to_string()

        elif ext == '.html':
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)

        elif ext == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        print(f"Error reading file: {e}")
        text = ""

    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""
    summary_type = request.form.get('summary_type', 'quick')

    # Handle uploaded file
    if 'file' in request.files and request.files['file']:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = extract_text(filepath)

    # Append pasted text if available
    pasted_text = request.form.get('text', '').strip()
    if pasted_text:
        text += "\n" + pasted_text

    if not text.strip():
        return jsonify({'error': 'No text provided for summarization.'}), 400

    # Choose summary length based on user's choice
    if summary_type == 'quick':
        max_len = 60
    else:
        max_len = 150

    try:
        result = summarizer(text, max_length=max_len, min_length=30, do_sample=False)
        summary = result[0]['summary_text']
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': f"Summarization failed: {str(e)}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
