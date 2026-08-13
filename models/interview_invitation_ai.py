from models.llama import ask_llama


def generate_interview_invitation(

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

Generate a professional interview invitation email.

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

The email should include:

• Greeting
• Congratulations for being shortlisted
• Interview details
• Instructions to join
• Closing with HR Team

Return only the email.
"""

    return ask_llama(prompt)