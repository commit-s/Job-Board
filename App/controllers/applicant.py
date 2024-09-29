from App.models import Applicant, Application, Listing, Job, Company
from App.database import db
from tabulate import tabulate
from datetime import date

# Submit a job application
def submit_application(applicant_id, listing_id, submission_date=date.today(), status='pending'):
    applicant = Applicant.query.get(applicant_id)
    listing = Listing.query.get(listing_id)
    if not applicant:
        return 1
    if not listing:
        return 2

    existing_application = Application.query.filter_by(applicant_id=applicant_id, listing_id=listing_id).first()
    if existing_application:
        return 3
    
    new_application = Application(applicant_id=applicant_id, listing_id=listing_id, submission_date=submission_date, status=status)
    db.session.add(new_application)
    db.session.commit()
    return new_application

# View applications for an applicant
def get_applications_for_applicant(applicant_id):
    applications = Application.query.filter_by(applicant_id=applicant_id).all()
    if not applications:
        return None

    table_data = []
    headers = ["Application ID", "Company", "Job", "Status", "Date Submitted"]
    for application in applications:
        listing = Listing.query.get(application.listing_id)
        job = Job.query.get(listing.job_id)
        company = Company.query.get(job.company_id)
        if not (listing and job and company):
            continue
        table_data.append([application.id, company.company_name, job.title, application.status, application.submission_date])

    return tabulate(table_data, headers, tablefmt="fancy_grid")

# View all applicants
def view_all_applicants():
    applicants = Applicant.query.all()
    if not applicants:
        return None

    table_data = []
    for applicant in applicants:
        application_count = Application.query.filter_by(applicant_id=applicant.id).count()
        table_data.append([applicant.id, applicant.username, applicant.name, application_count])
    headers = ["Applicant ID", "Username", "Name", "Applications"]
    return tabulate(table_data, headers, tablefmt="fancy_grid")
