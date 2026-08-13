from models.llama import ask_llama


def generate_rejection_email(

    candidate_name,
    job_title,
    rejection_reason,
    feedback,
    future_opportunity

):

    prompt = f"""
You are an HR Manager.

Generate a professional rejection email.

Candidate:
{candidate_name}

Job:
{job_title}

Reason:
{rejection_reason}

Feedback:
{feedback}

Future Opportunity:
{future_opportunity}

Return only the email.
"""

    return ask_llama(prompt)