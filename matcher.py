from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy
from functools import lru_cache
import spacy
from spacy.cli import download

try:
    spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")


nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens)

@lru_cache(maxsize=128)
def cached_preprocess(text):
    return preprocess(text)

def calculate_similarity(resume_texts, job_description):
    processed_texts = [cached_preprocess(text) for text in resume_texts]
    job_description = cached_preprocess(job_description)

    docs = [job_description] + processed_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarities
