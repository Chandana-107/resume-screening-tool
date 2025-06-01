# Automated Resume Screening Tool

A Automated resume screening tool implemented as a Streamlit app that ranks resumes based on a job description using NLP techniques (spaCy and TF-IDF). It supports uploading multiple PDF resumes, pasting a job description, and seeing resumes ranked by relevance.

## Features
- Upload multiple PDF resumes
- Paste a job description
- See resumes ranked by relevance
- Download ranking results as CSV

## Installation
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```
## Tech Stack

- **Frontend**: Streamlit + Custom CSS
- **Backend**: Python (NLP using SpaCy, Scikit-learn)
- **Database**: MongoDB
- **Others**: PyMuPDF, pandas
