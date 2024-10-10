from .user import create_user
from .job import create_job
from .listing import add_listing
from .application import submit_application

from App.data import companies, applicants, jobs, applications


from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    
    # Add applicant and employer that tests will be using
    create_user('gamefreak','password1', 'employer', 'Game Freak')
    create_user('jonathan_J','password1', 'applicant', 'Jonathan Joseph')

    # Populate Databse
    for username, password, name, user_type, company_name in companies:
        create_user(username, password, user_type, company_name)
    
    for username, password, name in applicants:
        create_user(username, password, 'applicant', name)

    for employer_id, job_name, salary, description, listing_date in jobs:
        job = create_job(employer_id, job_name, salary, description)
        add_listing(job.id, employer_id, listing_date)

    # Sample job applications
    for applicant_id, listing_id, submission_date, status in applications:
        submit_application(applicant_id, listing_id, submission_date, status)