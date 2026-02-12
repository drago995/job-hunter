import requests
import json
from config import LLM_MODEL, LLM_BASE_URL, RESUME

# Keywords you're interested in
TARGET_KEYWORDS = [
    "junior",
    "java",
    "spring",
    "spring boot",
    "react",
    "javascript",
    "python",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "docker",
    "git",
]

def evaluate_job_fit(job, resume=RESUME):
    """
    Simple keyword-based matching instead of LLM evaluation.
    Looks for target keywords in job title, company, description, and skills.
    Returns a score (0-100) based on keyword matches.
    """
    
    score = 0
    matches = []
    gaps = []
    
    # Combine all job info into searchable text (lowercase for case-insensitive matching)
    job_text = f"{job.get('title', '')} {job.get('description', '')} {' '.join(job.get('skills', []))}".lower()
    
    # Count keyword matches
    keyword_matches = 0
    for keyword in TARGET_KEYWORDS:
        if keyword.lower() in job_text:
            keyword_matches += 1
            matches.append(keyword.capitalize())
    
    # Calculate score based on keyword density
    score = min(100, (keyword_matches / len(TARGET_KEYWORDS)) * 100)
    
    # Bonus for having "junior" in title
    if "junior" in job.get('title', '').lower():
        score = min(100, score + 20)
    
    # Check for red flags (senior-only requirements)
    red_flags = ["senior", "5+ years", "10+ years", "lead", "architect"]
    has_red_flags = any(flag.lower() in job_text for flag in red_flags)
    if has_red_flags:
        score = max(0, score - 15)
    else:
        gaps.append("No experience requirement mismatch detected")
    
    evaluation = {
        "score": int(score),
        "matches": matches[:5],  # Top 5 matches
        "gaps": gaps,
        "recommendation": f"{'Good fit - apply!' if score >= 40 else 'Consider applying'} ({int(score)}/100)"
    }
    
    return evaluation


def evaluate_multiple_jobs(jobs, resume=RESUME, min_score=40):
    """
    Evaluate multiple jobs using keyword matching.
    Returns only those that meet the minimum score.
    """
    results = []
    
    for idx, job in enumerate(jobs):
        print(f"Evaluating job {idx + 1}/{len(jobs)}: {job.get('title', 'Unknown')}...")
        
        evaluation = evaluate_job_fit(job, resume)
        
        job_with_eval = {
            **job,
            "evaluation": evaluation
        }
        
        score = evaluation.get("score", 0)
        
        if score >= min_score:
            results.append(job_with_eval)
            print(f"  ✓ Score: {score} - MATCH!")
        else:
            print(f"  ✗ Score: {score} - Skip")
    
    return results


if __name__ == "__main__":
    # Test with a sample job
    test_job = {
        "title": "Junior Java Developer",
        "company": "TechCorp",
        "description": "Looking for a Junior Java developer with Spring Boot experience. Must know PostgreSQL and React.",
        "salary": "$50k-70k",
        "link": "https://example.com/job/123",
        "skills": ["Java", "Spring Boot", "PostgreSQL", "React"]
    }
    
    print("Testing keyword-based evaluator...")
    result = evaluate_job_fit(test_job)
    print(json.dumps(result, indent=2))

