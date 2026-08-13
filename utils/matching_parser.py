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


def parse_matching(response):

    data = {}

    data["score"] = extract("Match Score", response)

    data["matched"] = [
        x.strip()
        for x in extract("Matched Skills", response).split(",")
        if x.strip()
    ]

    data["missing"] = [
        x.strip()
        for x in extract("Missing Skills", response).split(",")
        if x.strip()
    ]

    data["suggestions"] = extract("Suggestions", response)

    return data