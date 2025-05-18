import pdfplumber
import spacy
import re
from typing import Dict, List, Set, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from skills import SKILLS, EDUCATION_KEYWORDS

# Load models
nlp = spacy.load("en_core_web_sm")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    return text

def preprocess_text(text: str) -> str:
    """Clean and preprocess text."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract entities using spaCy NER and custom rules."""
    doc = nlp(text)
    
    entities = {
        'PERSON': set(),
        'ORG': set(),
        'GPE': set(),
        'DATE': set(),
        'SKILLS': set(),
        'EDUCATION': set()
    }
    
    # Extract spaCy entities
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text.lower())
    
    # Extract skills
    text_lower = text.lower()
    for skill in SKILLS:
        if skill in text_lower:
            entities['SKILLS'].add(skill)
    
    # Extract education
    for edu in EDUCATION_KEYWORDS:
        if edu in text_lower:
            entities['EDUCATION'].add(edu)
    
    # Convert sets to sorted lists for JSON serialization
    return {k: sorted(list(v)) for k, v in entities.items()}

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts using Sentence-BERT."""
    # Encode texts
    embedding1 = sentence_model.encode([text1], convert_to_tensor=True)
    embedding2 = sentence_model.encode([text2], convert_to_tensor=True)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(
        embedding1.cpu().numpy(),
        embedding2.cpu().numpy()
    )[0][0]
    
    return float(similarity)

def analyze_resume_and_job(resume_text: str, job_description: str) -> Tuple[float, Dict, Dict]:
    """Main function to analyze resume and job description."""
    # Preprocess texts
    clean_resume = preprocess_text(resume_text)
    clean_jd = preprocess_text(job_description)
    
    # Calculate similarity score
    similarity_score = calculate_similarity(clean_resume, clean_jd)
    
    # Extract entities
    resume_entities = extract_entities(resume_text)
    jd_entities = extract_entities(job_description)
    
    return similarity_score, resume_entities, jd_entities 