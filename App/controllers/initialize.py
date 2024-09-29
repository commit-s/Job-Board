from .user import create_user, update_user, delete_user, get_all_users_table
from .applicant import submit_application, view_all_applicants, get_applications_for_applicant, get_available_applicants
from .company import view_all_companies
from .job import create_job, delete_job, update_job
from .listing import get_all_listings, get_company_listings
from .application import delete_application, update_application_status, view_applications_for_job

from App.data import companies, applicants, jobs, applications


from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    
    # Populate Databse
    for username, password, name, user_type, company_name in companies:
        create_user(username, password, name, user_type, company_name)
    
    for username, password, name in applicants:
        create_user(username, password, name, 'applicant', None)

    for company_id, job_name, salary, description, listing_date in jobs:
        create_job(company_id, job_name, salary, description, listing_date)

    # Sample job applications
    for applicant_id, listing_id, submission_date, status in applications:
        submit_application(applicant_id, listing_id, submission_date, status)