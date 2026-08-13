from models.llama import ask_llama

def ai_parse_resume(resume_text):

    prompt = f"""
YOU ARE AN EXPERT ATS RESUME PARSER.

EXTRACT ALL INFORMATION FROM THE RESUME.

RULES:
1. NEVER SKIP ANY SECTION.
2. IF A SECTION IS MISSING, WRITE "NOT AVAILABLE".
3. RETURN ONLY IN THE FORMAT BELOW.
4. DO NOT SUMMARIZE THE RESUME.
5. EXTRACT EVERY SKILL, PROJECT, EDUCATION, CERTIFICATION, EXPERIENCE, EMAIL, PHONE, LOCATION, GITHUB, LINKEDIN, AND SUMMARY.

CANDIDATE NAME:
EMAIL:
PHONE:
LOCATION:

SKILLS:
- Skill 1
- Skill 2

EDUCATION:
- Degree | College | Year

EXPERIENCE:
- Company | Role | Duration

PROJECTS:
- Project 1
- Project 2

CERTIFICATIONS:
- Certificate 1
- Certificate 2

SUMMARY:
3-5 SENTENCES

RESUME:
-----------------------
{resume_text}
-----------------------
"""

    response = ask_llama(prompt)

    return response