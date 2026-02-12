import json
from ollama import chat
from config import LLM_MODEL, RESUME

def generate_cover_letter(job, resume=RESUME, candidate_name="[Your Name]"):
    """
    Generate a tailored cover letter for a specific job posting.
    """
    
    prompt = f"""
Write a professional, concise cover letter for the following position. The letter should be personalized based on the job requirements and the candidate's experience.

CANDIDATE RESUME:
{resume}

JOB POSTING:
Title: {job.get('title', 'N/A')}
Company: {job.get('company', 'N/A')}
Description: {job.get('description', 'N/A')}

REQUIREMENTS:
- Make it 3-4 paragraphs
- Address the hiring manager as "Dear Hiring Manager"
- Highlight 2-3 relevant skills from the candidate's resume that match the job
- Show enthusiasm for the role and company
- End with a professional closing
- Keep it under 250 words

Write only the cover letter text, no explanations.
"""

    try:
        response = chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer. Write concise, personalized cover letters."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        cover_letter = response['message']['content'].strip()
        return {
            "success": True,
            "cover_letter": cover_letter,
            "job_title": job.get('title'),
            "company": job.get('company')
        }
            
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_cover_letters_for_matches(matched_jobs, resume=RESUME):
    """
    Generate cover letters for all matched jobs.
    """
    results = []
    
    for idx, job in enumerate(matched_jobs):
        print(f"Generating cover letter {idx + 1}/{len(matched_jobs)}: {job.get('title', 'Unknown')}...")
        
        cover_letter = generate_cover_letter(job, resume)
        
        job_with_letter = {
            **job,
            "cover_letter": cover_letter
        }
        
        results.append(job_with_letter)
    
    return results


def save_cover_letters(jobs_with_letters, filename="cover_letters.json"):
    """Save generated cover letters to file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs_with_letters, f, ensure_ascii=False, indent=2)
    print(f"Saved cover letters to {filename}")


if __name__ == "__main__":
    # Test with a sample job
    test_job = {
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "description": "Looking for a Senior Python developer with 5+ years experience in Django, FastAPI, and cloud deployment. Experience with AWS and Docker required.",
        "salary": "$80k-100k",
        "link": "https://example.com/job/123"
    }
    
    print("Testing cover letter generator...")
    result = generate_cover_letter(test_job)
    if result["success"]:
        print("\nGenerated Cover Letter:")
        print("=" * 50)
        print(result["cover_letter"])
    else:
        print(f"Error: {result['error']}")
