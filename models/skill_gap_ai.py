from models.llama import ask_llama


def analyze_skill_gap(candidate_resume, job_description):

    prompt = f"""
You are an AI Recruitment Assistant.

Candidate Resume:
{candidate_resume}

Job Description:
{job_description}

Compare the candidate with the job and respond EXACTLY in this format.

Existing Skills:
Python, SQL, Machine Learning

Missing Skills:
Java, AWS, Docker

Recommended Courses:
1. Java Programming - Oracle
2. AWS Cloud Practitioner
3. Docker Essentials

Learning Suggestions:
- Learn Java fundamentals.
- Gain AWS cloud experience.
- Practice Docker projects.

Rules:
1. Always include all four sections.
2. If no missing skills exist, write:

Missing Skills:
None

Recommended Courses:
None

Learning Suggestions:
Candidate already satisfies all required skills.

Do not write anything outside this format.
"""

    return ask_llama(prompt)