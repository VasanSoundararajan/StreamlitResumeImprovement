import streamlit as st
import pandas as pd
import re
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = " ".join([page.extract_text() or "" for page in pdf.pages])
    return text.strip()

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

# Function to extract text from images using OCR
def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image).strip()

# Function to extract details
def extract_details(text):
    name = text.split("\n")[0] if text else "Not Found"
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'\+?\d[\d\s()-]{8,}', text)
    linkedin_match = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[\w-]+', text)

    return {
        "Name": name if name.strip() else "Not Found",
        "Email": email_match.group(0) if email_match else "Not Found",
        "Phone": phone_match.group(0) if phone_match else "Not Found",
        "LinkedIn": linkedin_match.group(0) if linkedin_match else "Not Found"
    }

# Extract Skills
def extract_skills(text):
    skills_list = ["Python", "Django", "React", "SQL", "NoSQL", "Machine Learning", "AI", "UI/UX", "REST API", "Java"]
    detected_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return ", ".join(detected_skills) if detected_skills else "Not Found"

# Extract Experience
def extract_experience(text):
    match = re.search(r'(\d+)\s*(?:years?|yrs?)\s*experience', text, re.IGNORECASE)
    return f"{match.group(1)} years" if match else "Not Found"

# Extract Projects and Certifications
def extract_projects_certifications(text):
    count = len(re.findall(r'\b(project|certification|course)\b', text, re.IGNORECASE))
    return count if count > 0 else "Not Found"

# Check if Resume has Enough Details
def check_resume_completeness(details, skills, experience, projects):
    missing_sections = []
    if details["Name"] == "Not Found": missing_sections.append("Name")
    if details["Email"] == "Not Found": missing_sections.append("Email")
    if details["Phone"] == "Not Found": missing_sections.append("Phone")
    if details["LinkedIn"] == "Not Found": missing_sections.append("LinkedIn")
    if skills == "Not Found": missing_sections.append("Skills")
    if experience == "Not Found": missing_sections.append("Experience")
    if projects == "Not Found": missing_sections.append("Projects/Certifications")

    return missing_sections

# Function to determine file type and extract text accordingly
def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type in ["image/png", "image/jpeg", "image/jpg"]:
        return extract_text_from_image(file)
    else:
        return ""

# Rank Resumes (Unchanged)
def rank_resumes(job_description, resumes, resume_names):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

    experience_scores = [extract_experience(res) for res in resumes]
    skill_matches = [len(set(job_description.lower().split()) & set(res.lower().split())) for res in resumes]
    project_counts = [extract_projects_certifications(res) for res in resumes]

    ranking_df = pd.DataFrame({
        "Resume": resume_names,
        "Score": cosine_similarities,
        "Experience": experience_scores,
        "Skills Matched": skill_matches,
        "Projects": project_counts
    }).sort_values(by=["Score", "Experience", "Skills Matched", "Projects"], ascending=[False, False, False, False])

    return ranking_df

# Streamlit Web App
st.title("🔹 AI Resume Ranking & Completeness Checker")

# Job description input
job_description = st.text_area("Enter the job description")
uploaded_files = st.file_uploader("Upload Resumes (PDF, DOCX, PNG, JPEG)", type=["pdf", "docx", "png", "jpeg", "jpg"], accept_multiple_files=True)

if uploaded_files and job_description:
    resumes, resume_names, resume_details = [], [], []

    for file in uploaded_files:
        extracted_text = extract_text(file)
        if extracted_text:
            resumes.append(extracted_text)
            resume_names.append(file.name)

            details = extract_details(extracted_text)
            skills = extract_skills(extracted_text)
            experience = extract_experience(extracted_text)
            projects = extract_projects_certifications(extracted_text)

            missing_fields = check_resume_completeness(details, skills, experience, projects)
            resume_details.append({"Name": details["Name"], "Missing Fields": ", ".join(missing_fields) if missing_fields else "None"})

    # Display Resume Completeness
    st.subheader("Resume Completeness Check")
    st.write(pd.DataFrame(resume_details))

    # Display Resume Ranking (Remains Unchanged)
    results = rank_resumes(job_description, resumes, resume_names)
    st.subheader("Resume Ranking")
    st.write(results)

    # Select Resume for Improvement
    selected_resume = st.selectbox("Select a resume to suggest improvements", results["Resume"])
    
    if selected_resume:
        selected_index = resume_names.index(selected_resume)
        extracted_text = resumes[selected_index]
        
        details = extract_details(extracted_text)
        skills = extract_skills(extracted_text)
        experience = extract_experience(extracted_text)
        projects = extract_projects_certifications(extracted_text)

        missing_fields = check_resume_completeness(details, skills, experience, projects)

        # st.subheader("🔹 Suggested Improvements")
        # if not missing_fields:
        #     st.success("✅ This resume has all the necessary details.")
        # # else:
        # #     for field in missing_fields:
        # #         new_value = st.text_input(f"Add {field}:")
        # #         if new_value:
        # #             details[field] = new_value  # Update details in real-time
