from models.llama import ask_llama


def generate_interview_reminder(

    candidate_name,
    job_title,
    interview_type,
    interview_date,
    interview_time,
    interview_mode,
    meeting_link

):

    prompt = f"""
You are an HR Manager.

Generate a professional Interview Reminder Email.

Candidate Name:
{candidate_name}

Job Title:
{job_title}

Interview Type:
{interview_type}

Interview Date:
{interview_date}

Interview Time:
{interview_time}

Interview Mode:
{interview_mode}

Meeting Link / Venue:
{meeting_link}

The email should contain:

• Subject
• Greeting
• Reminder about interview
• Interview Details
• Instructions
• Best Wishes
• HR Team

Return only the email.
"""

    return ask_llama(prompt)