"""
Main Job Application Agent
Orchestrates job scraping, evaluation, cover letter generation, and tracking
"""

import json
from datetime import datetime
from job_scraper import scrape_poslovi_infostud, save_jobs_to_file, load_jobs_from_file
from job_evaluator import evaluate_multiple_jobs
from cover_letter_generator import generate_cover_letters_for_matches
from application_tracker import ApplicationTracker
from config import RESUME

class JobApplicationAgent:
    def __init__(self):
        self.tracker = ApplicationTracker()
        self.matched_jobs = []
        self.jobs_with_letters = []
    
    def run_full_pipeline(self, scrape_new=False, min_score=50, max_pages=5, limit=None):
        """
        Run the complete pipeline:
        1. Scrape jobs (or load cached)
        2. Filter out already applied jobs
        3. Evaluate jobs for fit
        4. Generate cover letters for matches
        5. Save results and display report
        """
        
        print("=" * 60)
        print("JOB APPLICATION AGENT - STARTING PIPELINE")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 1: Scraper
        print("STEP 1: SCRAPING JOBS")
        print("-" * 60)
        if scrape_new:
            print(f"Scraping jobs from poslovi.infostud.com ({max_pages} pages)...")
            jobs = scrape_poslovi_infostud(max_pages=max_pages, limit=limit)
            save_jobs_to_file(jobs)
            print(f"✓ Scraped {len(jobs)} jobs")
        else:
            jobs = load_jobs_from_file()
            print(f"✓ Loaded {len(jobs)} cached jobs")
        
        if not jobs:
            print("No jobs found!")
            return
        
        print()
        
        # Step 2: Filter already applied
        print("STEP 2: FILTERING ALREADY APPLIED JOBS")
        print("-" * 60)
        print(f"Already applied to {self.tracker.get_applied_count()} jobs")
        new_jobs = self.tracker.filter_new_jobs(jobs)
        print(f"✓ Found {len(new_jobs)} new jobs to evaluate")
        print()
        
        if not new_jobs:
            print("No new jobs to process!")
            return
        
        # Step 3: Evaluate jobs
        print("STEP 3: EVALUATING JOB FIT")
        print("-" * 60)
        print(f"Evaluating {len(new_jobs)} jobs (minimum score: {min_score})...")
        print()
        self.matched_jobs = evaluate_multiple_jobs(new_jobs, RESUME, min_score=min_score)
        print()
        print(f"✓ Found {len(self.matched_jobs)} matching jobs (score >= {min_score})")
        print()
        
        if not self.matched_jobs:
            print("No jobs matched your criteria.")
            return
        
        # Step 4: Generate cover letters
        print("STEP 4: GENERATING COVER LETTERS")
        print("-" * 60)
        self.jobs_with_letters = []
        for idx, job in enumerate(self.matched_jobs, 1):
            print(f"Generating cover letter {idx}/{len(self.matched_jobs)}: {job.get('title', 'Unknown')}...")
            
            from cover_letter_generator import generate_cover_letter
            cover_letter = generate_cover_letter(job, RESUME)
            
            job_with_letter = {
                **job,
                "cover_letter": cover_letter
            }
            
            self.jobs_with_letters.append(job_with_letter)
            
            # Save incrementally every 2 jobs
            if idx % 2 == 0:
                self.save_results()
                print(f"  (Auto-saved progress)")
        
        print(f"✓ Generated {len(self.jobs_with_letters)} cover letters")
        print()
        
        # Step 5: Save results
        print("STEP 5: SAVING RESULTS")
        print("-" * 60)
        self.save_results()
        print()
        
        # Step 6: Display summary
        self.display_summary()
    
    def save_results(self):
        """Save matched jobs with cover letters to file"""
        output_file = f"matched_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.jobs_with_letters, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved results to {output_file}")
    
    def display_summary(self):
        """Display a summary of matched jobs with cover letters"""
        print("=" * 60)
        print("MATCHED JOBS SUMMARY")
        print("=" * 60)
        
        for idx, job in enumerate(self.jobs_with_letters, 1):
            print()
            print(f"{idx}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
            print(f"   Link: {job.get('link', 'N/A')}")
            
            evaluation = job.get('evaluation', {})
            score = evaluation.get('score', 'N/A')
            print(f"   Match Score: {score}/100")
            
            cover_letter_data = job.get('cover_letter', {})
            if cover_letter_data.get('success'):
                print(f"   ✓ Cover letter generated")
                print()
                print("   COVER LETTER:")
                print("   " + "-" * 56)
                letter = cover_letter_data.get('cover_letter', '').replace('\n', '\n   ')
                print(f"   {letter}")
                print("   " + "-" * 56)
            else:
                print(f"   ✗ Cover letter generation failed: {cover_letter_data.get('error')}")
            
            print()
            print(f"   >>> NEXT STEP: Click the link above and apply manually <<<")
            print(f"   >>> Once applied, run: agent.mark_job_applied('{job.get('link')}') <<<")
    
    def mark_job_applied(self, job_link):
        """Mark a job as applied after manual submission"""
        # Find the job in our results
        job = next((j for j in self.jobs_with_letters if j.get('link') == job_link), None)
        if job:
            self.tracker.mark_applied(
                job.get('link'),
                job.get('title'),
                job.get('company'),
                notes="Applied with generated cover letter"
            )
            print(f"✓ Marked as applied: {job.get('title')} at {job.get('company')}")
        else:
            print(f"Job not found: {job_link}")
    
    def interactive_review(self):
        """Interactive mode to review and mark jobs as applied"""
        print("\n" + "=" * 60)
        print("INTERACTIVE APPLICATION REVIEW")
        print("=" * 60)
        
        for idx, job in enumerate(self.jobs_with_letters, 1):
            print()
            print(f"\n[{idx}/{len(self.jobs_with_letters)}] {job.get('title')} at {job.get('company')}")
            print(f"Link: {job.get('link')}")
            
            response = input("Have you applied to this job? (y/n/skip): ").lower().strip()
            
            if response == 'y':
                self.mark_job_applied(job.get('link'))
            elif response == 'skip':
                continue
            else:
                print(f"Skipping {job.get('title')}")


def main():
    agent = JobApplicationAgent()
    
    # Run the pipeline
    # scrape_new=True to scrape fresh jobs, False to use cached
    # min_score=40 for keyword matching (0-100 based on keyword matches)
    # max_pages=1 to scrape 1 page (~10 jobs)
    # limit=None to scrape all jobs (or set number to cap total jobs)
    try:
        agent.run_full_pipeline(
            scrape_new=True,
            min_score=40,
            max_pages=1,
            limit=None
        )
        
        # After review, can interactively mark jobs as applied
        # Uncomment to use interactive mode:
        # agent.interactive_review()
        
    except KeyboardInterrupt:
        print("\n✓ Agent stopped by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
