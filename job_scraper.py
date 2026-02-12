import json
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
from config import JOB_SITES

def scrape_poslovi_infostud(max_pages=5, limit=None):
    """
    Scrape job listings from poslovi.infostud.com across multiple pages
    Args:
        max_pages: Number of pages to scrape (default 5)
        limit: Total job limit across all pages (None = no limit)
    Returns list of job dicts with title, company, description, link, salary
    """
    jobs = []
    config = JOB_SITES["poslovi_infostud"]
    base_url = config["base_url"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            for page_num in range(1, max_pages + 1):
                if limit and len(jobs) >= limit:
                    break
                
                # Build URL with pagination - append page param to existing query params
                if "?" in base_url:
                    page_url = f"{base_url}&page={page_num}"
                else:
                    page_url = f"{base_url}?page={page_num}"
                print(f"Scraping page {page_num}: {page_url}")
                
                page.goto(page_url, wait_until="networkidle", timeout=30000)
                time.sleep(2)  # Wait for dynamic content to load
                
                # Select job cards using the correct infostud selector
                job_cards = page.query_selector_all(config["selector_job_card"])
                
                if not job_cards:
                    print(f"No jobs found on page {page_num}. Stopping pagination.")
                    break
                
                page_jobs_count = 0
                for idx, card in enumerate(job_cards):
                    if limit and len(jobs) >= limit:
                        break
                    
                    try:
                        # Extract job details using infostud HTML structure
                        title_elem = card.query_selector(config["selector_title"])
                        link_elem = card.query_selector(config["selector_link"])
                        
                        # Company is in a span after the building icon
                        company_spans = card.query_selector_all(config["selector_company"])
                        company = company_spans[0].inner_text() if len(company_spans) > 0 else "N/A"
                        
                        # Location is in the second location span
                        location = company_spans[1].inner_text() if len(company_spans) > 1 else "N/A"
                        
                        # Description is in the line-clamp paragraph
                        desc_elem = card.query_selector(config["selector_description"])
                        
                        # Skills are in the tag divs
                        skill_elems = card.query_selector_all(config["selector_skills"])
                        skills = [s.inner_text() for s in skill_elems if s.inner_text().strip() and s.inner_text() != "..."]
                        
                        job = {
                            "title": title_elem.inner_text() if title_elem else "N/A",
                            "company": company,
                            "location": location,
                            "description": desc_elem.inner_text() if desc_elem else "N/A",
                            "link": link_elem.get_attribute("href") if link_elem else "N/A",
                            "skills": skills,
                            "scraped_at": datetime.now().isoformat()
                        }
                        
                        # Extract just the clean URL without query params
                        if job["link"] and "?" in job["link"]:
                            job["link"] = job["link"].split("?")[0]
                        
                        jobs.append(job)
                        page_jobs_count += 1
                    except Exception as e:
                        print(f"Error parsing job card {idx} on page {page_num}: {e}")
                        continue
                
                print(f"  ✓ Scraped {page_jobs_count} jobs from page {page_num}")
                    
        finally:
            browser.close()
    
    return jobs


def save_jobs_to_file(jobs, filename="jobs_raw.json"):
    """Save scraped jobs to JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(jobs)} jobs to {filename}")


def load_jobs_from_file(filename="jobs_raw.json"):
    """Load jobs from JSON file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    print("Scraping jobs from poslovi.infostud.com...")
    jobs = scrape_poslovi_infostud(max_pages=3, limit=100)
    print(f"\nTotal jobs found: {len(jobs)}")
    for job in jobs[:3]:
        print(f"\n- {job['title']} at {job['company']}")
        print(f"  Location: {job['location']}")
        print(f"  Skills: {', '.join(job['skills'][:3])}")
        print(f"  Link: {job['link']}")
    save_jobs_to_file(jobs)
