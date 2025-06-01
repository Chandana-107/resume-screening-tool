import streamlit as st
from parser import extract_text_from_pdf
from matcher import calculate_similarity
from db import resumes_collection, job_collection, results_collection
import pandas as pd

st.set_page_config(page_title="Resume Screening Tool", layout="wide")

st.markdown(
    """
    <style>
    /* Background gradient animation */
    @keyframes gradientBackground {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    .stApp {
        background: linear-gradient(-45deg, #6a11cb, #2575fc, #6a11cb, #2575fc);
        background-size: 400% 400%;
        animation: gradientBackground 15s ease infinite;
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 2rem 3rem;
    }
    /* Title styling */
    .css-1v3fvcr h1 {
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #2575fc;
        text-shadow: 1px 1px 3px rgba(37, 117, 252, 0.6);
    }
    /* Text area and file uploader styling */
    .stTextArea, .stFileUploader {
        margin-bottom: 1.5rem;
        border-radius: 8px;
        padding: 0.75rem;
        background-color: rgba(255, 255, 255, 0.85);
        color: #000000;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    /* Label color for text area and file uploader */
    label {
    color: #000000 !important;
    font-weight: 700;
}

    /* Button styling */
    .stButton>button {
        background-color: #2575fc;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 8px rgba(37, 117, 252, 0.4);
    }
    .stButton>button:hover {
        background-color: #6a11cb;
        box-shadow: 0 6px 12px rgba(106, 17, 203, 0.6);
    }
    /* Ranked resumes section */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-top: 2rem;
        color: #000000;
    }
    /* Download button styling */
    .stDownloadButton>button {
        background-color: #6a11cb;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 8px rgba(106, 17, 203, 0.4);
        margin-top: 1rem;
    }
    .stDownloadButton>button:hover {
        background-color: #2575fc;
        box-shadow: 0 6px 12px rgba(37, 117, 252, 0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AUTOMATED RESUME SCREENING TOOL")

uploaded_jd = st.text_area("Job Description")
uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type="pdf", accept_multiple_files=True)

def save_to_db(uploaded_jd, uploaded_files, resume_texts, ranked, filenames):
    # Save Job Description
    jd_id = job_collection.insert_one({"description": uploaded_jd}).inserted_id

    # Save resumes
    resume_ids = []
    for i, file in enumerate(uploaded_files):
        text = resume_texts[i]
        doc = {
            "filename": file.name,
            "text": text
        }
        _id = resumes_collection.insert_one(doc).inserted_id
        resume_ids.append(_id)

    # Save results
    for i, (name, score) in enumerate(ranked):
        results_collection.insert_one({
            "job_id": jd_id,
            "resume_id": resume_ids[i],
            "filename": name,
            "score": round(score, 4)
        })

if st.button("Rank Resumes"):
    if not uploaded_jd or not uploaded_files:
        st.error("Please upload resumes and provide a job description.")
    else:
        with st.spinner("Processing resumes..."):
            resume_texts = []
            filenames = []

            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                resume_texts.append(text)
                filenames.append(file.name)

            scores = calculate_similarity(resume_texts, uploaded_jd)
            ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)

            st.write("### Ranked Resumes")
            for name, score in ranked:
                st.write(f"**{name}** — {round(score * 100, 2)}% match")

            # Save to DB
            save_to_db(uploaded_jd, uploaded_files, resume_texts, ranked, filenames)

            # Provide download option
            df = pd.DataFrame(ranked, columns=["Filename", "Match Score"])
            df["Match Score"] = df["Match Score"].apply(lambda x: f"{round(x * 100, 2)}%")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Ranked Results as CSV",
                data=csv,
                file_name="ranked_resumes.csv",
                mime="text/csv"
            )
       