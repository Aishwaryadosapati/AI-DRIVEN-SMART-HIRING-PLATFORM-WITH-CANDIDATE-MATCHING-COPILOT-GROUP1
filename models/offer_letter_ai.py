from models.llama import ask_llama


def generate_offer_letter(

    candidate_name,
    designation,
    employee_id,
    salary,
    joining_date,
    department,
    work_location,
    employment_type

):

    prompt = f"""
You are an HR Manager.

Generate a professional Offer Letter.

Candidate:
{candidate_name}

Employee ID:
{employee_id}

Designation:
{designation}

Salary:
{salary}

Joining Date:
{joining_date}

Department:
{department}

Location:
{work_location}

Employment Type:
{employment_type}

Return a complete professional offer letter.
"""

    return ask_llama(prompt)