from models.llama import ask_llama


def generate_technical_questions(skills, resume_text):

    prompt = f"""
You are a Senior Technical Interviewer.

Generate exactly 10 technical interview questions.

Candidate Resume:
{resume_text}

Required Skills:
{skills}

Generate questions on:
- Programming
- SQL
- Problem Solving
- Projects
- Job-specific skills

Return ONLY the questions.
"""

    return ask_llama(prompt)