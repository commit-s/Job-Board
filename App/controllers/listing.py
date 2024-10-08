from App.models import Listing, Job
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

# Get a specific listing
def get_listing(listing_id):
    return Listing.query.get(listing_id)

# Get all listings
def get_all_listings():
    return Listing.query.all()

# Get all company listings
def get_company_listings(employer_id):
    return Listing.query.filter_by(employer_id=employer_id).all()

# Add a job to listings
def add_listing(job_id, employer_id, date):
    if not Job.query.get(job_id):
        return None
    
    existing_listing = Listing.query.filter_by(job_id=job_id).first()
    if existing_listing:
        print(f"Listing already exists for job '{job_id}'")
        return existing_listing
    
    try:
        listing = Listing(job_id, employer_id, date)
        db.session.add(listing)
        db.session.commit()
        return listing
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error occured during job listing: {e}')
        return None
        