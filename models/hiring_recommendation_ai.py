from models.llama import ask_llama


def generate_hiring_recommendation(resume_text, job_description):

    prompt = f"""
You are an AI HR Recruitment Assistant.

Candidate Resume:
{resume_text}

Job Description:
{job_description}

Compare the resume with the job description.

Return ONLY in the following format.

Decision:
Hire

Reason:
Candidate has strong technical skills and satisfies most job requirements.

Strengths:
Python
SQL
Machine Learning

Weaknesses:
AWS
Docker

Interview Questions:
Explain OOP concepts.
What is SQL JOIN?
Difference between REST API and SOAP?

Rules:
1. Always include all sections.
2. Decision should be only one of:
Hire
Hold
Reject
3. Do not add any extra explanation.
"""

    return ask_llama(prompt)