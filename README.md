# Job Application Agent

An autonomous job application system that scrapes job postings, evaluates fit, generates cover letters, and tracks applications.

## Features

- **Job Scraping**: Scrapes jobs from poslovi.infostud
- **Intelligent Evaluation**: user hard coded words to calculate percentage of match
- **Cover Letter Generation**: Creates tailored cover letters for each job
- **Application Tracking**: Prevents duplicate applications
- **Application**: returns link for the job and the cover letter (must apply manually)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Install and Start Ollama

- Download from [ollama.ai](https://ollama.ai)
- Run Ollama (must be running for the agent to work)
- Pull llama3 model: `ollama pull llama3:8b`

### 3. Add Your Resume

Edit `config.py` and fill in the `RESUME` variable with your actual resume text:

```python
RESUME = """
NAME: John Doe
EMAIL: john@example.com
PHONE: +1-555-0123

PROFESSIONAL SUMMARY:
Experienced software developer with 5+ years in Python and web development.

SKILLS:
- Python (Django, FastAPI)
- JavaScript/React
- PostgreSQL, Redis
- Docker, AWS
- Git, Linux

EXPERIENCE:
Senior Developer at TechCorp (2021-2024)
- Led development of microservices architecture
- Managed team of 4 developers

...rest of resume
"""
```

## Usage

### Quick Start

```bash
python agent.py
```


1. Scrape jobs from poslovi.infostud.hr
2. Filter out already applied jobs
3. Evaluate jobs against your resume (matches score >= 50)
4. Generate cover letters for matches
5. Display results with links to apply manually

### Configuration

Edit `agent.py` line 60:

```python
agent.run_full_pipeline(
    scrape_new=True,   # Set False to use cached jobs
    min_score=50,      # Minimum match score (0-100)
    limit=30           # Number of jobs to scrape (None for all)
)
```

### Marking Jobs as Applied

After you manually apply on the website, mark it as applied:

```python
# In Python
from agent import JobApplicationAgent
agent = JobApplicationAgent()
agent.mark_job_applied("https://...")

# Or use interactive mode:
agent.interactive_review()
```

## File Structure

- `config.py` - Configuration (resume, LLM settings)
- `job_scraper.py` - Scrapes poslovi.infostud.hr
- `job_evaluator.py` - Evaluates job-resume fit
- `cover_letter_generator.py` - Generates cover letters
- `application_tracker.py` - Tracks applied jobs
- `agent.py` - Main orchestrator

## Output Files

- `jobs_raw.json` - Raw scraped jobs
- `matched_jobs_YYYYMMDD_HHMMSS.json` - Matched jobs with evaluations and cover letters
- `applied_jobs.json` - History of applied jobs
- `application_report.json` - Application statistics


## Note on Automation

This agent does NOT automatically submit applications. This is intentional because:
- Many job sites require manual verification (CAPTCHA, confirmation emails)
- You should review each application before submitting
- The agent generates everything; you click the submit button

The workflow is: Review → Click Apply → Mark as Applied

## Future Enhancements

- Email integration to auto-send cover letters
- Resume tailoring per job
- Job board integrations (LinkedIn, Indeed, GitHub Jobs)
- Application success rate tracking
- Interview scheduling

