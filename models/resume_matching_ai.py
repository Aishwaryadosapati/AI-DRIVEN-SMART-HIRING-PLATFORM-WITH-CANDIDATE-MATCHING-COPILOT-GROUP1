from models.llama import ask_llama


def match_resume(resume_text, job_description):

    prompt = f"""
You are an AI Recruitment Assistant.

Compare the following Resume with the Job Description.

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY in this format.

Match Score: 85

Matched Skills:
Python, SQL, Machine Learning

Missing Skills:
Docker, Kubernetes, AWS

Suggestions:
Learn Docker, Kubernetes and AWS to improve your resume.
"""

    return ask_llama(prompt)