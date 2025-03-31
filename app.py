from flask import Flask, render_template, request
import fitz  # PyMuPDF for PDF text extraction
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Folder to store uploaded resumes
UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load SBERT Model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

def rank_resumes(job_description, resume_texts, resume_filenames):
    """Compute similarity scores and rank resumes."""
    job_embedding = model.encode([job_description])
    resume_embeddings = model.encode(resume_texts)
    
    similarities = cosine_similarity(job_embedding, resume_embeddings)[0] * 100  # Convert to percentage
    
    ranked_resumes = sorted(zip(resume_filenames, similarities), key=lambda x: x[1], reverse=True)
    
    return [{"name": filename, "score": round(score, 2), "rank": i+1} for i, (filename, score) in enumerate(ranked_resumes)]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_description = request.form["job_description"]
        uploaded_files = request.files.getlist("resume")
        
        resume_texts = []
        resume_filenames = []
        
        for file in uploaded_files:
            if file and file.filename.endswith(".pdf"):
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)
                
                text = extract_text_from_pdf(file_path)
                resume_texts.append(text)
                resume_filenames.append(file.filename)
        
        if resume_texts:
            ranked_resumes = rank_resumes(job_description, resume_texts, resume_filenames)
            return render_template("results.html", ranked_resumes=ranked_resumes)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
