import streamlit as st
import json
from utils import analyze_resume_and_job, extract_text_from_pdf

# Page config
st.set_page_config(
    page_title="ATS Resume & JD Matcher",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    /* Increase base font size */
    .stMarkdown, .stTextArea textarea {
        font-size: 1.1rem !important;
    }
    /* Make headers larger */
    h1 {
        font-size: 2.5rem !important;
    }
    h2 {
        font-size: 2rem !important;
    }
    h3, .stSubheader {
        font-size: 1.5rem !important;
    }
    /* Style buttons */
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        font-size: 1.2rem !important;
        padding: 0.75rem !important;
    }
    /* Style JSON output */
    .json-output {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 1.1rem !important;
    }
    /* Make metrics larger */
    .stMetric {
        font-size: 1.3rem !important;
    }
    .stMetricLabel {
        font-size: 1.1rem !important;
    }
    /* Style warnings and success messages */
    .stAlert {
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📄 ATS Resume & JD Matcher")
st.markdown("""
    Upload your resume and paste a job description to:
    - Calculate semantic similarity score
    - Extract key entities (skills, education, etc.)
    - Optimize your resume for ATS systems
""")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📎 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200
    )

# Process button
if st.button("🔍 Analyze"):
    if uploaded_file is not None and job_description:
        try:
            with st.spinner("Processing..."):
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Analyze texts
                similarity_score, resume_entities, jd_entities = analyze_resume_and_job(
                    resume_text,
                    job_description
                )
                
                # Display results
                st.header("Results")
                
                # Display match score
                score_percentage = round(similarity_score * 100, 2)
                st.metric(
                    "Resume ↔ Job Description Match Score",
                    f"{score_percentage}%"
                )
                
                # Create columns for entities
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📄 Resume Entities")
                    st.json(resume_entities)
                
                with col2:
                    st.subheader("💼 Job Description Entities")
                    st.json(jd_entities)
                
                # Recommendations
                st.subheader("📋 Recommendations")
                missing_skills = set(jd_entities['SKILLS']) - set(resume_entities['SKILLS'])
                if missing_skills:
                    st.warning(
                        "Consider adding these skills from the job description: " +
                        ", ".join(missing_skills)
                    )
                if score_percentage < 70:
                    st.warning(
                        "Your resume's match score is below 70%. Consider updating your "
                        "resume to better match the job description's key terms and requirements."
                    )
                if score_percentage >= 70:
                    st.success(
                        "Good match! Your resume appears to be well-aligned with "
                        "the job description."
                    )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload a resume PDF and paste a job description.") 