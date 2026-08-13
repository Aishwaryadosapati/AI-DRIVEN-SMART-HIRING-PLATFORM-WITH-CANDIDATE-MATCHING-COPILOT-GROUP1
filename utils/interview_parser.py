import re


def parse_questions(response):

    questions = []

    for line in response.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^\d+\.\s*", "", line)
        line = re.sub(r"^-\s*", "", line)

        if len(line) > 5:

            questions.append(line)

    return questions