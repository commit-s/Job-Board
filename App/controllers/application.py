from App.models import Application, Applicant
from App.database import db
from tabulate import tabulate

# Delete an application
def delete_application(applicant_id, application_id):
    application = Application.query.get(application_id)
    if not (application and application.applicant_id == applicant_id):
        return None
    
    db.session.delete(application)
    db.session.commit()
    return application

# View the status of an application
def view_application_status(application_id):
    application = Application.query.get(application_id)
    if not application:
        return None
    return application.view_status()

# Update application status (e.g., Accepted, Rejected)
def update_application_status(application_id, new_status):
    application = Application.query.get(application_id)
    if not application:
        return None
    
    application.status = new_status.lower()
    db.session.commit()
    return application

# View all applications for a listing
def view_applications_for_job(listing_id):
    applications = Application.query.filter_by(listing_id=listing_id).all()
    if not applications:
        return None

    table_data = []
    headers = ["Application ID", "Applicant", "Status", "Date Submitted"]
    for application in applications:
        applicant = Applicant.query.get(application.applicant_id)
        if not applicant:
            continue
        table_data.append([application.id, applicant.name, application.status, application.submission_date])

    return tabulate(table_data, headers, tablefmt="fancy_grid")
