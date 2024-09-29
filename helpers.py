from App.models import Company, Job, Listing
from App.controllers import (
    get_all_users_table, view_all_companies, view_all_applicants,
    get_all_listings, get_company_listings, view_applications_for_job, get_available_applicants
    )

# helpers.py
def center_title(title, table):
    table_lines = table.split('\n')
    max_line_length = max(len(line) for line in table_lines)
    title_length = len(title)

    if title_length < max_line_length:
        padding = (max_line_length - title_length) // 2
        return ' ' * padding + title
    return title

def display_all_users():
    user_table = get_all_users_table()
    if user_table:
        print(center_title("Users", user_table))
        print(user_table)

def display_all_companies():
    company_table = view_all_companies()
    if company_table:
        print(center_title("Companies", company_table))
        print(company_table)

def display_all_applicants():
    applicant_table = view_all_applicants()
    if applicant_table:
        print(center_title("Applicants", applicant_table))
        print(applicant_table)

def display_available_applicants(listing_id):
    applicant_table = get_available_applicants(listing_id)
    if applicant_table:
        print(center_title("Applicants", applicant_table))
        print(applicant_table)

def display_all_jobs():
    job_table = get_all_listings()
    if job_table:
        print(center_title("Jobs", job_table))
        print(job_table)

def display_company_jobs(company_id):
    jobs = get_company_listings(company_id)
    if jobs:
        company_name = Company.query.get(company_id).company_name
        print(center_title(f"Jobs from Company '{company_name}'", jobs))
        print(jobs)

def display_all_applicants_for_job(listing_id):
    applicant_table = view_applications_for_job(listing_id)
    if applicant_table:
        job_title = Job.query.get(Listing.query.get(listing_id).job_id).title
        company_name = Company.query.get(Listing.query.get(listing_id).company_id).company_name
        print(center_title(f"Applications for Job '{job_title}' by '{company_name}'", applicant_table))
        print(applicant_table)