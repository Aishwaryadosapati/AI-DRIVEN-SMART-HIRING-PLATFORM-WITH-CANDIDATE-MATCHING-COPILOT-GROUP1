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


def to_list(text):

    if not text:

        return []

    if text.lower() == "none":

        return []

    return [
        x.strip("-•1234567890. ").strip()
        for x in text.split("\n")
        if x.strip()
    ]


def parse_skill_gap(response):

    existing = extract(
        "Existing Skills",
        response
    )

    missing = extract(
        "Missing Skills",
        response
    )

    courses = extract(
        "Recommended Courses",
        response
    )

    suggestions = extract(
        "Learning Suggestions",
        response
    )

    return {

        "existing_skills": to_list(existing),

        "missing_skills": to_list(missing),

        "courses": courses,

        "suggestions": suggestions

    }