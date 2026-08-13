# AI Recruitment & Talent Management Copilot - Agent Guide

## Project Overview

This is a **Streamlit-based AI recruitment platform** that automates hiring workflows using AI. It provides resume analysis, candidate matching, skill gap analysis, and recruitment analytics.

**Stack**: Python 3, Streamlit, Pandas, Plotly

**Run**: `streamlit run app.py`

---

## Architecture

### Current Structure: Compact Flat Layout

The project uses a **compact flat folder structure** with all Python modules in the root directory. This design:
- Minimizes navigation overhead for simple features
- Makes module dependencies visible at a glance
- Works well for Streamlit's page-based architecture where each module implements a `show()` function

### Module Organization

| Category | Modules | Purpose |
|----------|---------|---------|
| **Core Workflow** | `resume.py`, `job_description.py`, `matching.py` | Resume upload, job posting, candidate-job matching |
| **Analysis & Ranking** | `resume_analysis.py`, `candidate_ranking.py`, `skill_gap.py` | Deep analysis of candidate profiles |
| **Insights & Reports** | `analytics.py`, `dashboard.py`, `hiring_recommendation.py` | Metrics, visualizations, hiring decisions |
| **AI Features** | `resume_chat.py`, `email_generator.py`, `interview_questions.py` | AI-powered candidate interactions |
| **Data Models** | `candidate_profile.py` | Candidate data structures |
| **Utilities** | `settings.py`, `style.css` | Configuration and styling |
| **Entry Point** | `app.py` | Streamlit main app with navigation |

### Pattern: Page Module Interface

Each page module follows this convention:
```python
def show():
    st.title("Page Title")
    # Implementation
```

This is called from `app.py` based on sidebar navigation.

---

## Key Files

- **[app.py](app.py)** - Main Streamlit entry point; defines navigation and page routing
- **[requirements.txt](requirements.txt)** - Python dependencies (streamlit, pandas, plotly)
- **[style.css](style.css)** - Custom CSS styling
- **[data/](data/)** - Data directory (resumes, jobs, reports)

---

## Common Tasks

### Adding a New Feature Page

1. Create a new module (e.g., `new_feature.py`) with a `show()` function
2. Import in `app.py`: `import new_feature`
3. Add to sidebar options in `app.py`
4. Add route: `elif page == "Feature Name": new_feature.show()`

### Working with Candidate Data

- Candidate profiles are defined in `candidate_profile.py`
- Resume data is stored in `data/resumes/`
- Use `resume_analysis.py` for profile extraction and `matching.py` for ranking

### Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Access at `http://localhost:8501`

---

## Development Notes

### Related Files to Watch
- `resume_analysis.py` ↔ `resume.py` (analysis vs. upload) - note potential duplication in naming
- `resume.matching.py` ↔ `matching.py` - consolidation candidate
- `candidate_ranking.py` - Currently placeholder ("Milestone 2")

### Future Refactoring Opportunity

Consider reorganizing into feature-based folders for scalability:
```
pages/
  resume/
  matching/
  analytics/
  settings/
utils/
data/
```

This would reduce cognitive load as the project grows beyond ~20 modules.

---

## Agent Tips

- **Navigation**: Use `app.py` to understand feature hierarchy
- **Data flow**: Resume Upload → Analysis → Matching → Ranking → Analytics
- **Styling**: Central in `style.css`; all pages use the same theme
- **Configuration**: Check `settings.py` for configurable parameters
