# 🧠 Document Summarizer Web App

This is a web-based document summarizer built with Python, Flask, and Hugging Face Transformers. It allows users to upload or paste content from various file types and receive an AI-generated summary — even for long documents!

---

## 🚀 Features

- ✅ Upload `.txt`, `.pdf`, `.docx`, `.md`, `.html`, and `.csv` files
- 📝 Paste custom text directly
- 🔄 Choose between **Quick** or **Detailed** summaries
- ⚡ Handles long documents with no character limit (chunking system)
- 💡 Clean, responsive web interface

---

## 📂 Supported File Types

- `.txt` (auto detects encoding)
- `.pdf`
- `.docx`
- `.csv`
- `.html`
- `.md` (Markdown)

---

## ⚙️ Setup Instructions

### 1. Clone or Download the Project

Unzip the provided folder or clone this repository.

### 2. Set Up a Python Virtual Environment (optional)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
