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
def get_employer_listings(employer_id):
    return Listing.query.filter_by(employer_id=employer_id).all()

# Add a job to listings
def add_listing(job_id, employer_id, date):
    if not Job.query.get(job_id):
        return None, 1
    
    existing_listing = Listing.query.filter_by(job_id=job_id).first()
    if existing_listing:
        print(f"Listing already exists for job '{job_id}'")
        return existing_listing, 1
    
    try:
        listing = Listing(job_id, employer_id, date)
        db.session.add(listing)
        db.session.commit()
        return listing, 0
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error occured during job listing: {e}')
        return None, 1
    
# Remove a listing
def remove_listing(listing_id):
    listing = get_listing(listing_id)
    if not listing:
        return None
    db.session.delete(listing)
    db.session.commit()
    return listing
        