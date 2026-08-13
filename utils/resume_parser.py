import re


def extract_email(text):

    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    return match.group() if match else ""


def extract_phone(text):

    match = re.search(r'(\+91[- ]?)?[6-9]\d{9}', text)

    return match.group() if match else ""


def extract_linkedin(text):

    match = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

    return match.group() if match else ""


def extract_github(text):

    match = re.search(r'https?://(www\.)?github\.com/[^\s]+', text)

    return match.group() if match else ""


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:

            if "resume" not in line.lower():

                return line

    return "Unknown"
SKILLS = [

"Python","Java","C","C++","SQL","HTML","CSS",

"JavaScript","React","Node.js","Angular",

"Flask","Django","FastAPI","Spring Boot",

"TensorFlow","PyTorch","Machine Learning",

"Deep Learning","OpenCV","Git","Docker",

"AWS","Azure","GCP","MongoDB","Power BI",

"Tableau","Excel","Pandas","NumPy"

]


def extract_skills(text):

    found=[]

    lower=text.lower()

    for skill in SKILLS:

        if skill.lower() in lower:

            found.append(skill)

    return sorted(list(set(found)))
EDUCATION = [

"B.Tech",

"M.Tech",

"B.E",

"M.E",

"Bachelor",

"Master",

"Engineering",

"Diploma",

"PhD"

]


def extract_education(text):

    result=[]

    for item in EDUCATION:

        if item.lower() in text.lower():

            result.append(item)

    return result
PROJECTS = [

"Project",

"Developed",

"Implemented",

"Designed",

"Application",

"System"

]


def extract_projects(text):

    result=[]

    for item in PROJECTS:

        if item.lower() in text.lower():

            result.append(item)

    return result
CERTS=[

"AWS",

"Oracle",

"Google",

"Cisco",

"Microsoft",

"NPTEL",

"Infosys",

"Coursera",

"Udemy"

]


def extract_certifications(text):

    result=[]

    for item in CERTS:

        if item.lower() in text.lower():

            result.append(item)

    return result
def extract_experience(text):

    pattern=r'(\d+)\+?\s*(years|year|yrs|yr)'

    match=re.findall(pattern,text,re.IGNORECASE)

    if match:

        return match[0][0]+" Years"

    return "Fresher"
def calculate_score(skills, education, projects, certifications, experience=""):

    score = 0

    # Skills (40)
    if skills:
        score += min(len(skills) * 2, 40)

    # Education (20)
    if education:
        score += 20

    # Projects (20)
    if projects:
        score += min(len(projects) * 10, 20)

    # Certifications (10)
    if certifications:
        score += min(len(certifications) * 2, 10)

    # Experience (10)
    if experience and experience.lower() not in ["", "not mentioned", "fresher"]:
        score += 10

    return min(score, 100)
def recommendation(score):

    if score>=80:

        return "Hire"

    elif score>=60:

        return "Hold"

    return "Reject"