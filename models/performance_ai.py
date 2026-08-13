from models.llama import ask_llama


def generate_performance_review(

    employee_name,
    designation,
    performance_rating,
    kpi_score,
    attendance,
    goal_completion,
    manager_feedback

):

    prompt = f"""
You are an HR Performance Manager.

Employee Name:
{employee_name}

Designation:
{designation}

Performance Rating:
{performance_rating}/5

KPI Score:
{kpi_score}

Attendance:
{attendance}%

Goal Completion:
{goal_completion}%

Manager Feedback:
{manager_feedback}

Generate:

1. Employee Performance Review

2. Strengths

3. Areas of Improvement

4. Promotion Recommendation

Return only the review.
"""

    return ask_llama(prompt)