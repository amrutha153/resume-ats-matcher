# Resume & Job Description Matcher (ATS Optimization)

A web application that helps candidates optimize their resumes for ATS (Applicant Tracking Systems) by comparing them with job descriptions using NLP techniques.

## Features

- Resume PDF text extraction
- Job Description analysis
- Semantic similarity scoring
- Named Entity Recognition (NER)
- Skills matching
- Education detection
- Real-time web interface

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

3. Run the application:
```bash
streamlit run app.py
```

## How to Use

1. Upload your resume in PDF format
2. Paste the job description in the text area
3. Click "Process" to analyze
4. View the match score and extracted entities

## Technologies Used

- Streamlit: Web interface
- Sentence-BERT: Semantic similarity
- spaCy: Named Entity Recognition
- pdfplumber: PDF text extraction
- scikit-learn: Cosine similarity computation 