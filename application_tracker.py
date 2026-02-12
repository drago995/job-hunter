import json
from datetime import datetime
from pathlib import Path

class ApplicationTracker:
    """
    Tracks which jobs have been applied to, preventing duplicate applications.
    """
    
    def __init__(self, filename="applied_jobs.json"):
        self.filename = filename
        self.load()
    
    def load(self):
        """Load applied jobs from file"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"applied": []}
    
    def save(self):
        """Save applied jobs to file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def mark_applied(self, job_link, job_title, company, notes=""):
        """Mark a job as applied"""
        applied = {
            "link": job_link,
            "title": job_title,
            "company": company,
            "applied_at": datetime.now().isoformat(),
            "notes": notes
        }
        
        # Check if already applied
        if self.has_applied(job_link):
            print(f"Already applied to: {job_title} at {company}")
            return False
        
        self.data["applied"].append(applied)
        self.save()
        print(f"✓ Marked as applied: {job_title} at {company}")
        return True
    
    def has_applied(self, job_link):
        """Check if already applied to a job"""
        return any(job["link"] == job_link for job in self.data["applied"])
    
    def get_applied_jobs(self):
        """Get list of all applied jobs"""
        return self.data["applied"]
    
    def get_applied_count(self):
        """Get count of applied jobs"""
        return len(self.data["applied"])
    
    def filter_new_jobs(self, jobs):
        """
        Filter out jobs that have already been applied to.
        Returns only new jobs.
        """
        new_jobs = []
        for job in jobs:
            if not self.has_applied(job.get("link", "")):
                new_jobs.append(job)
            else:
                print(f"Skipping already applied: {job.get('title')} at {job.get('company')}")
        
        return new_jobs
    
    def export_report(self, filename="application_report.json"):
        """Export a report of all applications"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"Report exported to {filename}")


if __name__ == "__main__":
    tracker = ApplicationTracker()
    
    # Test adding an application
    tracker.mark_applied(
        "https://example.com/job/123",
        "Python Developer",
        "TechCorp",
        "Applied via email"
    )
    
    # Check if applied
    print(f"Applied: {tracker.has_applied('https://example.com/job/123')}")
    print(f"Total applied: {tracker.get_applied_count()}")
    
    # Export report
    tracker.export_report()
