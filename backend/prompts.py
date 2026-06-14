ATS_KNOWLEDGE_BASE = """
ATS (Applicant Tracking System) Best Practices:

1. Format & Structure
   - Use standard section headers: Contact, Summary, Experience, Education, Skills
   - Avoid tables, text boxes, headers/footers, and multi-column layouts
   - Use simple fonts (Arial, Calibri, Times New Roman)
   - Save as PDF or DOCX; avoid images of text

2. Keywords & Skills
   - Include industry-specific keywords from the job description
   - List technical skills, tools, certifications explicitly
   - Use both acronyms and full terms (e.g., "ML" and "Machine Learning")
   - Mirror language from target job postings

3. Experience Section
   - Use reverse chronological order
   - Start bullets with strong action verbs (Led, Built, Improved, Delivered)
   - Quantify achievements with numbers and percentages
   - Include company name, job title, dates, and location

4. Contact Information
   - Place name, phone, email, LinkedIn at the top
   - Use a professional email address
   - Include city/state if relevant

5. Education
   - List degree, institution, graduation year
   - Include relevant coursework or honors if applicable

6. Common ATS Failures
   - Creative section names ("My Journey" instead of "Experience")
   - Graphics, icons, or skill bars
   - Missing keywords for the target role
   - Inconsistent date formats
   - Spelling and grammar errors
"""

ATS_ANALYSIS_PROMPT = """You are an expert ATS (Applicant Tracking System) resume analyst.

Use the retrieved resume context and ATS best practices below to evaluate the resume.

## ATS Best Practices
{ats_knowledge}

## Retrieved Resume Sections (most relevant chunks)
{retrieved_context}

## Full Resume Text
{resume_text}

## Similarity Scores (cosine similarity vs ATS criteria)
{similarity_scores}

Analyze the resume and respond ONLY with valid JSON in this exact format:
{{
  "overall_score": <number 0-100>,
  "categories": {{
    "format_structure": {{"score": <0-100>, "feedback": "<string>"}},
    "keywords_skills": {{"score": <0-100>, "feedback": "<string>"}},
    "experience": {{"score": <0-100>, "feedback": "<string>"}},
    "contact_education": {{"score": <0-100>, "feedback": "<string>"}}
  }},
  "strengths": ["<string>", "<string>"],
  "improvements": ["<string>", "<string>", "<string>"],
  "summary": "<2-3 sentence overall assessment>"
}}

Be specific and actionable. Base scores on real ATS parsing behavior.
"""

RETRIEVAL_QUERIES = [
    "resume format structure sections headers layout",
    "skills keywords technical certifications tools",
    "work experience achievements quantified results action verbs",
    "contact information email phone linkedin education degree",
    "ATS compatibility parsing issues tables graphics columns",
]
