from models.llama import ask_llama


def generate_hr_questions(resume_text, job_title):

    prompt = f"""
You are an HR Interviewer.

Generate 10 HR interview questions.

Candidate Resume:
{resume_text}

Job Role:
{job_title}

Questions should assess:

- Communication
- Behaviour
- Teamwork
- Leadership
- Career Goals
- Problem Solving
- Adaptability

Return ONLY the questions.
"""

    return ask_llama(prompt)