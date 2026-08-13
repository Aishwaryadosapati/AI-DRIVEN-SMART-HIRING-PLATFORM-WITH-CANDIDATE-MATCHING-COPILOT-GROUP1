# 🤖 AI-Driven Smart Hiring Platform with Candidate Matching Copilot

An AI-powered recruitment and talent management platform designed to support recruiters throughout the hiring lifecycle — from job creation and resume analysis to candidate matching, interviews, communication, onboarding, employee management, and talent management.

## 🎯 Project Overview

The AI-Driven Smart Hiring Platform provides a centralized dashboard for managing recruitment activities.

The platform combines:

- Streamlit for the web application
- Python for application logic
- SQLite for recruitment data
- Ollama with Llama 3.2 for local AI capabilities
- Pandas for data processing
- AI-assisted recruitment workflows

The system is designed as a prototype for an intelligent internal HR recruitment tool.

## 🚀 Key Features

### 1. 📊 Dashboard
Provides an overview of recruitment activities and key statistics such as:

- Total candidates
- Jobs
- Interviews
- Joined candidates
- Recruitment status

### 2. 💼 Job Management

Recruiters can:

- Create job openings
- Add job descriptions
- Define required skills
- Set experience requirements
- Set ATS score requirements
- Manage job openings and status

### 3. 📄 Resume Management

The platform supports:

- Resume upload
- Resume parsing
- Resume analysis
- Skill extraction
- Education extraction
- Experience extraction
- Certification extraction
- ATS scoring

### 4. 👤 Candidate Profile

Recruiters can view candidate information including:

- Personal details
- Resume information
- Skills
- Experience
- Education
- Projects
- Certifications
- ATS score
- Recommendation
- Candidate status

### 5. 🎯 Candidate Matching

Candidates can be matched against job requirements using:

- Required skills
- Resume information
- ATS score
- Experience
- Job requirements

Candidates can then be ranked according to their suitability.

### 6. 📅 Interview Management

The system supports interview scheduling and management for multiple stages, including:

- AI Interview
- Technical Interview
- HR Interview
- Final Managerial Interview

Interview details include:

- Interviewer
- Date
- Time
- Interview mode
- Meeting link
- Status
- Feedback

### 7. 🤖 AI Communication

The platform supports AI-assisted communication for:

- Interview invitation emails
- Interview reminder emails
- Offer letter emails
- Rejection emails
- Welcome emails

### 8. 💬 Resume Chat

Recruiters can interact with uploaded resume information using an AI-powered chat interface.

### 9. 🚀 Onboarding

The onboarding module manages:

- Employee ID
- Designation
- Department
- Reporting manager
- Joining date
- Emergency contact
- Document verification
- Onboarding status

### 10. 👨‍💼 Employee Management

HR users can manage employee information including:

- Employee details
- Department
- Designation
- Manager
- Status
- Employee directory
- Employee analytics

### 11. 🌟 Talent Management

The Talent Management module focuses on employee performance.

It includes:

- Performance rating
- KPI score
- Attendance
- Goal completion
- Manager feedback
- AI performance review
- Promotion recommendation
- HR notes

## 🧠 AI Technology

The project uses a locally hosted Large Language Model.

### Ollama + Llama 3.2

Llama 3.2 is run locally through Ollama.

The AI layer supports features such as:

- Resume analysis
- Job description analysis
- Interview question generation
- Resume chat
- Hiring recommendations
- Performance review generation
- AI-assisted communication

Running the model locally helps reduce dependency on external cloud APIs.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application UI |
| SQLite | Database |
| Ollama | Local LLM runtime |
| Llama 3.2 | Generative AI |
| Pandas | Data processing |
| Plotly | Data visualization |
| python-dotenv | Environment variable management |
| SMTP | Email communication |

## 🏗️ Project Structure

```text
AI-DRIVEN-SMART-HIRING-PLATFORM/
│
├── app.py
├── api.py
├── login.py
│
├── assets/
│
├── models/
│   ├── llama.py
│   ├── ai_resume_parser.py
│   ├── resume_matching_ai.py
│   ├── hiring_recommendation_ai.py
│   ├── interview_questions_ai.py
│   ├── performance_ai.py
│   └── ...
│
├── pages/
│   ├── dashboard.py
│   ├── job_management.py
│   ├── resume_management.py
│   ├── candidate_profile.py
│   ├── interview_management.py
│   ├── ai_communication.py
│   ├── onboarding.py
│   ├── employee_management.py
│   ├── talent_management.py
│   └── ...
│
├── utils/
│   ├── database.py
│   ├── email_sender.py
│   ├── email_service.py
│   ├── matching_parser.py
│   ├── resume_parser.py
│   └── ...
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md



## 📸 Application Screenshots

### 🏠 Dashboard
![Dashboard](SCREENSHOTS/dashboard.png)

### 💼 Job Management
![Job Management](SCREENSHOTS/job_management.png)

### 📄 Resume Management
![Resume Management](SCREENSHOTS/resume_management.png)

### 👤 Candidate Profile
![Candidate Profile](SCREENSHOTS/candidate_profile.png)

### 🎯 Resume Matching
![Resume Matching](SCREENSHOTS/resume_matching.png)

### 🎤 Interview Management
![Interview Management](SCREENSHOTS/interview_management.png)

### 🤖 AI Copilot
![AI Copilot](SCREENSHOTS/copilot.png)

### 💬 Resume Chat
![Resume Chat](SCREENSHOTS/resume_chat.png)

### 👥 Employee Management
![Employee Management](SCREENSHOTS/employee_management.png)

### 🚀 Onboarding
![Onboarding](SCREENSHOTS/onboarding.png)

### 🎯 Talent Management
![Talent Management](SCREENSHOTS/talent_management.png)