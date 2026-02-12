# Your resume - hardcoded as text (SANITIZED)
RESUME = """
NAME: Your Name
EMAIL: your.email@example.com
PHONE: +381-XXX-XXX

PROFESSIONAL SUMMARY:
Recent computer science graduate with strong fundamentals in Java and web development.
Completed multiple academic projects and internships involving full-stack development.
Motivated to launch a career in software development and contribute to a dynamic team.

SKILLS:
Programming Languages: Java, JavaScript, C, Python, R, SQL
Frameworks & Libraries: Spring Boot, Spring, React, Laravel
Databases: PostgreSQL, MySQL, MongoDB
Tools & Platforms: Git, Maven, Docker, IntelliJ

EXPERIENCE:
Teaching Instructor
Company Name
Jan 2024 — Present
• Taught Machine Learning, R programming and Probability & Statistics to students
• Designed exercises and practical examples to help students understand core concepts

Artist Manager
Company Name
• Coordinated performance opportunities for musicians
• Communicated with venues and organized schedules

EDUCATION:
University Name
Bachelor's in Computer Science
2019 — 2025

PROJECTS:
Internship Management System | Spring Boot, React, PostgreSQL
• Web-based system for managing internships with registration and notifications

Java Coursework Projects | core Java, JDBC, SQL, Multithreading
• Developed database-driven applications and applied design patterns
"""

# LLM Configuration
LLM_MODEL = "llama3"
LLM_BASE_URL = "http://localhost:11434"  

# Job board configuration
JOB_SITES = {
    "poslovi_infostud": {
        "base_url": "https://poslovi.infostud.com/oglasi-za-posao-java-developer?scope=srpoz",
        "selector_job_card": "div.search-job-card",
        "selector_title": "h2",
        "selector_company": "p span",
        "selector_location": "p span",
        "selector_description": "p.line-clamp-3",
        "selector_link": "a[href*='/posao/']",
        "selector_skills": "div.bg-neutrals-1 span",
        "max_pages": 1
    }
}
