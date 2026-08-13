import sqlite3
import os




DB_PATH = "database/recruitment.db"


def get_connection():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        job_id INTEGER,

        name TEXT,

        email TEXT UNIQUE,

        phone TEXT,

        location TEXT,

        resume_path TEXT,

        resume_text TEXT,

        skills TEXT,

        experience TEXT,

        education TEXT,

        projects TEXT,

        certifications TEXT,

        resume_score INTEGER DEFAULT 0,

        recommendation TEXT,

        candidate_status TEXT DEFAULT 'Applied',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")
    

    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    job_title TEXT,

    department TEXT,

    location TEXT,

    experience TEXT,

    employment_type TEXT,

    salary TEXT,

    skills TEXT,

    description TEXT,

    minimum_ats_score INTEGER,

    openings INTEGER,

    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")


    

    cursor.execute("""

CREATE TABLE IF NOT EXISTS interview_questions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER,

    job_id INTEGER,

    interview_type TEXT,

    questions TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(candidate_id) REFERENCES candidates(id),

    FOREIGN KEY(job_id) REFERENCES jobs(id)

)

""")


    cursor.execute("""

        CREATE TABLE IF NOT EXISTS interviews(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER,

    job_id INTEGER,

    candidate_name TEXT,

    candidate_email TEXT,

    interview_type TEXT,

    interviewer TEXT,

    interview_date TEXT,

    interview_time TEXT,

    duration TEXT,

    interview_mode TEXT,

    meeting_link TEXT,

    status TEXT,

    feedback TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(candidate_id) REFERENCES candidates(id),

    FOREIGN KEY(job_id) REFERENCES jobs(id)

)

""") 

    cursor.execute("""

CREATE TABLE IF NOT EXISTS employees(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER,

    employee_id TEXT,

    employee_name TEXT,

    email TEXT,

    phone TEXT,

    designation TEXT,

    department TEXT,

    manager TEXT,

    joining_date TEXT,

    location TEXT,

    emergency_contact TEXT,

    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(candidate_id) REFERENCES candidates(id)

)

""")

    cursor.execute("""

CREATE TABLE IF NOT EXISTS employee_performance(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id TEXT,

    employee_name TEXT,

    performance_rating INTEGER,

    kpi_score INTEGER,

    attendance INTEGER,

    goal_completion INTEGER,

    manager_feedback TEXT,

    ai_review TEXT,

    promotion_status TEXT,

    hr_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")




    

    conn.commit()

    conn.close()

    migrate_jobs_table()

    migrate_candidates_table()

    migrate_interviews_table() 



def add_candidate(
    job_id,
    name,
    email,
    phone,
    location,
    resume_path,
    resume_text
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if candidate already exists
    cursor.execute(
        "SELECT id FROM candidates WHERE email=?",
        (email,)
    )

    row = cursor.fetchone()

    if row:

        candidate_id = row["id"]

        cursor.execute("""
        UPDATE candidates
        SET
            job_id=?,
            name=?,
            phone=?,
            location=?,
            resume_path=?,
            resume_text=?
        WHERE id=?
        """,
        (
            job_id,
            name,
            phone,
            location,
            resume_path,
            resume_text,
            candidate_id
        ))

    else:

        cursor.execute("""
        INSERT INTO candidates(
            job_id,
            name,
            email,
            phone,
            location,
            resume_path,
            resume_text
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            job_id,
            name,
            email,
            phone,
            location,
            resume_path,
            resume_text
        ))

        candidate_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return candidate_id


def update_candidate_analysis(
    candidate_id,
    skills,
    experience,
    education,
    projects,
    certifications,
    score,
    recommendation
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE candidates
    SET
        skills=?,
        experience=?,
        education=?,
        projects=?,
        certifications=?,
        resume_score=?,
        recommendation=?
    WHERE id=?
    """,
    (
        skills,
        experience,
        education,
        projects,
        certifications,
        score,
        recommendation,
        candidate_id
    ))

    # Save the update count BEFORE running another query
    rows = cursor.rowcount

    conn.commit()

    print("Rows Updated:", rows)

    cursor.execute(
        "SELECT * FROM candidates WHERE id=?",
        (candidate_id,)
    )

    record = cursor.fetchone()

    if record:
        print(dict(record))

    conn.close()

    return rows


def get_all_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



def get_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates WHERE id=?",
        (candidate_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row

def get_candidate_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM candidates"

    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def add_job(

    job_title,
    department,
    location,
    experience,
    employment_type,
    salary,
    skills,
    description,
    minimum_ats_score,
    openings,
    status

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO jobs(

        job_title,
        department,
        location,
        experience,
        employment_type,
        salary,
        skills,
        description,
        minimum_ats_score,
        openings,
        status

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?)

    """,(

        job_title,
        department,
        location,
        experience,
        employment_type,
        salary,
        skills,
        description,
        minimum_ats_score,
        openings,
        status

    ))

    conn.commit()

    conn.close()

def get_all_jobs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def delete_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM jobs WHERE id=?",

        (job_id,)

    )

    conn.commit()

    conn.close()

def get_job_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_resume_scores():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT resume_score FROM candidates"

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_recommendations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT recommendation FROM candidates"

    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ==========================
# Interview Functions
# ==========================





def get_interview_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM interviews"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def delete_interview(interview_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM interviews WHERE id=?",
        (interview_id,)
    )

    conn.commit()
    conn.close()




def get_joined_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE candidate_status='Joined'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_candidate_status_counts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT candidate_status, COUNT(*) AS total
        FROM candidates
        GROUP BY candidate_status
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def migrate_jobs_table():

    conn = get_connection()
    cursor = conn.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(jobs)")
    columns = [row[1] for row in cursor.fetchall()]

    if "minimum_ats_score" not in columns:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN minimum_ats_score INTEGER DEFAULT 80
        """)

    if "openings" not in columns:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN openings INTEGER DEFAULT 1
        """)

    conn.commit()
    conn.close()


def migrate_candidates_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(candidates)")
    columns = [row[1] for row in cursor.fetchall()]

    if "job_id" not in columns:
        cursor.execute("""
            ALTER TABLE candidates
            ADD COLUMN job_id INTEGER
        """)

    conn.commit()
    conn.close()


def migrate_interviews_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(interviews)")
    columns = [row[1] for row in cursor.fetchall()]

    new_columns = {

        "candidate_id": "INTEGER",
        "job_id": "INTEGER",
        "candidate_name": "TEXT",
        "candidate_email": "TEXT",
        "interview_type": "TEXT",
        "duration": "TEXT",
        "interview_mode": "TEXT",
        "feedback": "TEXT"

    }

    for column, datatype in new_columns.items():

        if column not in columns:

            cursor.execute(
                f"ALTER TABLE interviews ADD COLUMN {column} {datatype}"
            )

    conn.commit()
    conn.close()


def get_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM jobs WHERE id=?",
        (job_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None

def update_candidate_ats(candidate_id, ats_score):

    conn = get_connection()
    cursor = conn.cursor()

    # Get candidate's job
    cursor.execute(
        "SELECT job_id FROM candidates WHERE id=?",
        (candidate_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return

    job = get_job(row["job_id"])

    cutoff = job["minimum_ats_score"]

    if ats_score >= cutoff:
        recommendation = "Shortlisted"
        status = "Shortlisted"
    else:
        recommendation = "Rejected"
        status = "Rejected"

    cursor.execute("""
        UPDATE candidates
        SET
            resume_score=?,
            recommendation=?,
            candidate_status=?
        WHERE id=?
    """,
    (
        ats_score,
        recommendation,
        status,
        candidate_id
    ))

    conn.commit()
    conn.close()


def get_shortlisted_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE candidate_status='Shortlisted'
        ORDER BY name
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def get_all_candidates_with_job():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE job_id IS NOT NULL
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_candidates_by_job(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE job_id=?
        ORDER BY resume_score DESC
    """, (job_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def delete_candidate(candidate_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    conn.commit()
    conn.close()

def get_candidate_by_id(candidate_id):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    return dict(candidate) if candidate else None

def get_candidates_by_status(status):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE candidate_status = ?
        ORDER BY resume_score DESC
        """,
        (status,)
    )

    candidates = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return candidates

def update_candidate_status(candidate_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET candidate_status = ?
        WHERE id = ?
        """,
        (status, candidate_id)
    )

    conn.commit()
    conn.close()


def get_total_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_shortlisted_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE candidate_status = 'Shortlisted'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_rejected_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE candidate_status = 'Rejected'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count







def get_interview(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM interviews

        WHERE candidate_id=?

        ORDER BY id DESC

        LIMIT 1
        """,
        (candidate_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return dict(row)

    return None




from models.llama import ask_llama


def generate_technical_questions(skills, resume_text):

    prompt = f"""
You are a Senior Technical Interviewer.

Generate exactly 10 technical interview questions.

Candidate Resume:
{resume_text}

Required Skills:
{skills}

Generate questions on:
- Programming
- SQL
- Problem Solving
- Projects
- Job-specific skills

Return ONLY the questions.
"""

    return ask_llama(prompt)







def save_invitation_status(
    candidate_id,
    interview_round,
    interview_date,
    interview_time,
    interview_mode,
    invitation_status,
    recruiter_notes
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET
            interview_type=?,
            interview_date=?,
            interview_time=?,
            interview_mode=?,
            status=?,
            feedback=?
        WHERE candidate_id=?
        """,
        (
            interview_round,
            interview_date,
            interview_time,
            interview_mode,
            invitation_status,
            recruiter_notes,
            candidate_id
        )
    )

    conn.commit()
    conn.close()

def save_invitation_status(
    candidate_id,
    interview_round,
    interview_date,
    interview_time,
    interview_mode,
    invitation_status,
    recruiter_notes
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET
            interview_type=?,
            interview_date=?,
            interview_time=?,
            interview_mode=?,
            status=?,
            feedback=?
        WHERE candidate_id=?
        """,
        (
            interview_round,
            interview_date,
            interview_time,
            interview_mode,
            invitation_status,
            recruiter_notes,
            candidate_id
        )
    )

    conn.commit()
    conn.close()

def save_offer_status(
    candidate_id,
    employee_id,
    designation,
    salary,
    joining_date,
    department,
    work_location,
    employment_type,
    offer_status,
    hr_notes
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET
            status=?,
            feedback=?
        WHERE candidate_id=?
        """,
        (
            offer_status,
            hr_notes,
            candidate_id
        )
    )

    conn.commit()
    conn.close()


def save_welcome_status(
    candidate_id,
    employee_id,
    joining_date,
    reporting_manager,
    work_location,
    welcome_status,
    hr_notes
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET
            status=?,
            feedback=?
        WHERE candidate_id=?
        """,
        (
            welcome_status,
            hr_notes,
            candidate_id
        )
    )

    conn.commit()
    conn.close()




def save_rejection_status(
    candidate_id,
    rejection_status,
    rejection_reason,
    feedback,
    future_opportunity,
    hr_notes
):

    conn = get_connection()
    cursor = conn.cursor()

    remarks = f"""
Reason: {rejection_reason}

Feedback: {feedback}

Future Opportunity: {"Yes" if future_opportunity else "No"}

HR Notes: {hr_notes}
"""

    cursor.execute(
        """
        UPDATE interviews
        SET
            status=?,
            feedback=?
        WHERE candidate_id=?
        """,
        (
            rejection_status,
            remarks,
            candidate_id
        )
    )

    conn.commit()
    conn.close()



def schedule_interview(
    candidate_id,
    job_id,
    interview_type,
    interviewer,
    interview_date,
    interview_time,
    duration,
    mode,
    meeting_link,
    status,
    remarks
):

    conn = get_connection()
    cursor = conn.cursor()

    # Get candidate details
    cursor.execute(
        """
        SELECT name, email
        FROM candidates
        WHERE id=?
        """,
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    candidate_name = candidate["name"]
    candidate_email = candidate["email"]

    cursor.execute(
        """
        INSERT INTO interviews(

            candidate_name,
            candidate_email,
            interviewer,
            interview_date,
            interview_time,
            interview_mode,
            meeting_link,
            status,
            feedback,
            candidate_id,
            job_id,
            interview_type,
            duration

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,
        (

            candidate_name,
            candidate_email,
            interviewer,
            interview_date,
            interview_time,
            mode,
            meeting_link,
            status,
            remarks,
            candidate_id,
            job_id,
            interview_type,
            duration

        )

    )

    conn.commit()
    conn.close()


def get_all_interviews():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM interviews
        ORDER BY interview_date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



def save_interview_questions(

    candidate_id,
    job_id,
    interview_type,
    questions

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_questions(

            candidate_id,

            job_id,

            interview_type,

            questions

        )

        VALUES(?,?,?,?)

        """,

        (

            candidate_id,

            job_id,

            interview_type,

            questions

        )

    )

    conn.commit()

    conn.close()




def get_saved_interview_questions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM interview_questions

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



def save_employee(
    candidate_id,
    employee_id,
    employee_name,
    email,
    phone,
    designation,
    department,
    manager,
    joining_date,
    location,
    emergency_contact,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees(

            candidate_id,
            employee_id,
            employee_name,
            email,
            phone,
            designation,
            department,
            manager,
            joining_date,
            location,
            emergency_contact,
            status

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)

        """,
        (

            candidate_id,
            employee_id,
            employee_name,
            email,
            phone,
            designation,
            department,
            manager,
            joining_date,
            location,
            emergency_contact,
            status

        )

    )

    conn.commit()
    conn.close()



def get_all_employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]



def get_employee_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_employee(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM employees
        WHERE employee_id=?
        """,
        (employee_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


def update_employee(
    employee_id,
    designation,
    department,
    manager,
    phone,
    location,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET
            designation=?,
            department=?,
            manager=?,
            phone=?,
            location=?,
            status=?
        WHERE employee_id=?
        """,
        (
            designation,
            department,
            manager,
            phone,
            location,
            status,
            employee_id
        )
    )

    conn.commit()
    conn.close()


def delete_employee(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM employees
        WHERE employee_id=?
        """,
        (employee_id,)
    )

    conn.commit()
    conn.close()



def save_performance(

    employee_id,

    employee_name,

    performance_rating,

    kpi_score,

    attendance,

    goal_completion,

    manager_feedback,

    ai_review,

    promotion_status,

    hr_notes

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO employee_performance(

            employee_id,

            employee_name,

            performance_rating,

            kpi_score,

            attendance,

            goal_completion,

            manager_feedback,

            ai_review,

            promotion_status,

            hr_notes

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

    """,

    (

        employee_id,

        employee_name,

        performance_rating,

        kpi_score,

        attendance,

        goal_completion,

        manager_feedback,

        ai_review,

        promotion_status,

        hr_notes

    )

    )

    conn.commit()

    conn.close()