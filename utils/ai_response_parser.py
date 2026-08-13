import re


def extract(field, text):

    pattern = rf"{field}\s*:\s*(.*?)(?=\n[A-Za-z ]+\s*:|\Z)"

    match = re.search(
        pattern,
        text,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


def make_list(text):

    if not text:
        return []

    text = text.replace("•", "\n")
    text = text.replace("-", "\n")
    text = text.replace(";", "\n")

    items = []

    for line in text.split("\n"):

        line = line.strip()

        if line:

            items.append(line)

    return items


def parse_ai_response(response):

    data = {}

    data["name"] = extract("Candidate Name", response)

    data["email"] = extract("Email", response)

    data["phone"] = extract("Phone", response)

    data["location"] = extract("Location", response)

    data["skills"] = make_list(
        extract("Skills", response)
    )

    data["education"] = make_list(
        extract("Education", response)
    )

    data["projects"] = make_list(
        extract("Projects", response)
    )

    data["certifications"] = make_list(
        extract("Certifications", response)
    )

    data["experience"] = extract(
        "Experience",
        response
    )

    data["summary"] = extract(
        "Summary",
        response
    )

    return data

def parse_hiring_recommendation(response):

    recommendation = "Hold"
    reason = ""

    rec_match = re.search(
        r"Recommendation\s*:\s*(.*)",
        response,
        re.IGNORECASE
    )

    if rec_match:
        recommendation = rec_match.group(1).strip()

    reason_match = re.search(
        r"Reason\s*:\s*(.*)",
        response,
        re.DOTALL | re.IGNORECASE
    )

    if reason_match:
        reason = reason_match.group(1).strip()

    return {
        "recommendation": recommendation,
        "reason": reason
    }