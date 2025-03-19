# AI Resume Ranking & Completeness Checker

This project is a Streamlit-based web application that uses AI techniques to analyze resumes, rank them based on job descriptions, and check for missing details in the resumes.

## Features
✅ Extracts text from various file types (PDF, DOCX, PNG, JPEG).  
✅ Identifies key details like **Name**, **Email**, **Phone**, and **LinkedIn**.  
✅ Extracts technical skills, experience, and projects/certifications.  
✅ Ranks resumes based on similarity to the job description using **TF-IDF** and **Cosine Similarity**.  
✅ Highlights missing resume sections for improvement suggestions.  

---

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/ai-resume-checker.git
   cd ai-resume-checker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```sh
   streamlit run main.py
   ```

---

## Usage
1. Enter the **Job Description** in the provided text area.  
2. Upload multiple resumes in **PDF**, **DOCX**, **PNG**, or **JPEG** format.  
3. The app will display:
   - **Resume Completeness Check** with missing sections for each resume.  
   - **Resume Ranking** sorted by similarity score, experience, and other key factors.  
4. Select a resume to receive detailed suggestions for improvement.

---

## Sample Output
```
🔹 Resume Completeness Check
| Name        | Missing Fields        |
|--------------|------------------------|
| John Doe     | None                   |
| Jane Smith   | Email, LinkedIn        |

🔹 Resume Ranking
| Resume       | Score  | Experience | Skills Matched | Projects |
|---------------|--------|-------------|-----------------|------------|
| John_Doe.pdf | 0.87   | 3 years     | 7                | 4          |
| Jane_Smith.docx | 0.75 | 2 years     | 5                | 3          |
```

---

## Future Enhancements
- Add support for extracting content from `.txt` files.  
- Implement improved NLP techniques for better skill detection.  
- Introduce feedback-based learning for personalized resume suggestions.  

---

## License
This project is licensed under the **MIT License**.

