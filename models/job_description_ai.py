from models.llama import ask_llama


def generate_job_description(

    job_title,

    department,

    experience,

    skills

):

    prompt = f"""
You are an HR Recruitment Expert.

Generate a professional job description.

Job Title: {job_title}

Department: {department}

Experience: {experience}

Required Skills: {skills}

Return the following sections:

1. Job Summary

2. Roles and Responsibilities

3. Required Skills

4. Preferred Qualifications

5. Benefits

Keep the description professional and suitable for a company hiring page.
"""

    return ask_llama(prompt)