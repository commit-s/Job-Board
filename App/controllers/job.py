from App.models import Job, Company, Listing
from App.database import db
from datetime import date

# Create a new job
def create_job(company_id, title, salary, description, listing_date=date.today()):
    company = Company.query.get(company_id)
    if not company:
        return None

    new_job = Job(title=title, salary=salary, description=description, company_id=company_id)
    db.session.add(new_job)
    db.session.commit()

    new_listing = Listing(job_id=new_job.id, company_id=company_id, listing_date=listing_date)
    db.session.add(new_listing)
    db.session.commit()
    return new_job

# Delete a job
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return None

    db.session.delete(job)
    db.session.commit()
    return job

# Update a job's details
def update_job(job_id, title=None, salary=None, description=None):
    job = Job.query.get(job_id)
    if not job:
        return None

    if title:
        job.title = title
    if salary:
        job.salary = salary
    if description:
        job.description = description

    db.session.commit()
    return job
