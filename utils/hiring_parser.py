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

    if not text or text.lower() == "none":
        return []

    return [
        x.strip("-•1234567890. ").strip()
        for x in text.split("\n")
        if x.strip()
    ]


def parse_hiring_recommendation(response):

    return {

        "decision": extract("Decision", response),

        "reason": extract("Reason", response),

        "strengths": to_list(
            extract("Strengths", response)
        ),

        "weaknesses": to_list(
            extract("Weaknesses", response)
        ),

        "questions": to_list(
            extract("Interview Questions", response)
        )

    }