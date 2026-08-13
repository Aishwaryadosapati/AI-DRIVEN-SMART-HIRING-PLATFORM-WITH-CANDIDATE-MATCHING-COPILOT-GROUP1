from models.llama import ask_llama


def generate_questions(

    interview_type,
    difficulty,
    question_count,
    skills,
    resume_text

):

    prompt = f"""
You are an expert interviewer.

Generate exactly {question_count} interview questions.

Interview Type:
{interview_type}

Difficulty:
{difficulty}

Candidate Resume:
{resume_text}

Required Skills:
{skills}

Instructions:

- If AI Interview:
Generate aptitude, logical reasoning and basic technical MCQs.

- If Technical Interview:
Generate programming, SQL, projects and coding questions.

- If HR Interview:
Generate behavioural, communication and leadership questions.

- If Final Manager Interview:
Generate project discussion, business understanding, leadership and decision-making questions.

Return ONLY the questions.
"""

    return ask_llama(prompt)