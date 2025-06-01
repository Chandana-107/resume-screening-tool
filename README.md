# Automated Resume Screening Tool

A Streamlit app that ranks resumes based on a job description using NLP (spaCy + TF-IDF).

## Features
- Upload multiple PDF resumes
- Paste a job description
- See resumes ranked by relevance

## Installation
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```