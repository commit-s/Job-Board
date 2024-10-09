from App.models import Application
from .listing import get_listing
from .user import get_user
from App.database import db
from datetime import date
from sqlalchemy.exc import SQLAlchemyError


# get specific application
def get_application(application_id):
    return Application.query.get(application_id)

# get applications for job listing
def get_applications_for_job(listing_id):
    return Application.query.filter_by(listing_id=listing_id)

def set_application_status(application_id, status=None):
    application = get_application(application_id)
    if not application or status is None:
        return None
    application.status = status
    db.session.commit()
    return application

# Submit a job application given the applicant's id and job's listing id
def submit_application(applicant_id, listing_id, submission_date=None, status='pending'):
    submission_date = submission_date or date.today() # ensure default date (today) is consistent
    applicant = get_user(applicant_id)
    listing = get_listing(listing_id)

    if not applicant or not listing:
        return None, 1

    existing_application = Application.query.filter_by(applicant_id=applicant_id, listing_id=listing_id).first()
    if existing_application:
        print("Application already exists")
        return existing_application, 1
    
    try:
        new_application = Application(applicant_id, listing_id, submission_date, status)
        db.session.add(new_application)
        db.session.commit()
        return new_application, 0
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error occured: {e}')
        return None, 1
    
# Delete an application
def delete_application(applicant_id, application_id):
    application = get_application(application_id)
    if not (application and application.applicant_id == applicant_id):
        return None
    
    db.session.delete(application)
    db.session.commit()
    return application