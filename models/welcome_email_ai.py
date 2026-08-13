from models.llama import ask_llama


def generate_welcome_email(

    employee_name,
    employee_id,
    designation,
    joining_date,
    reporting_manager,
    reporting_time,
    location,
    documents

):

    prompt = f"""
You are an HR Manager.

Generate a professional Welcome Email.

Employee Name:
{employee_name}

Employee ID:
{employee_id}

Designation:
{designation}

Joining Date:
{joining_date}

Reporting Manager:
{reporting_manager}

Reporting Time:
{reporting_time}

Office Location:
{location}

Documents:
{documents}

The email should include:

• Welcome message
• Congratulations
• Joining details
• Reporting manager
• Documents to carry
• Best wishes
• HR Team

Return only the email.
"""

    return ask_llama(prompt)