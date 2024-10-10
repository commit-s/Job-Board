from App.models import Job, Employer
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

# Get a specific job
def get_job(job_id):
    return Job.query.get(job_id)

# Get all jobs
def get_all_jobs():
    return Job.query.all()

# Get all jobs from company
def get_employer_jobs(employer_id):
    return Job.query.filter_by(employer_id=employer_id).all()

# Create a new job
def create_job(employer_id, title, salary, description):
    if not Employer.query.get(employer_id):
        return None
    
    existing_job = Job.query.filter_by(employer_id=employer_id, title=title, description=description).first()
    if existing_job:
        print('Similar Job already exists')
        return existing_job.id
    
    try:
        new_job = Job(employer_id, title, salary, description)
        db.session.add(new_job)
        db.session.commit()
        return new_job
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error occured during job creation: {e}')
        return None

# Update a job's details
def update_job(job_id, title=None, salary=None, description=None):
    job = Job.query.get(job_id)
    if not job:
        return None

    if title is not None:
        job.title = title
    if salary is not None:
        job.salary = salary
    if description is not None:
        job.description = description

    db.session.commit()
    return job

# Delete a job
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return None

    db.session.delete(job)
    db.session.commit()
    return job

