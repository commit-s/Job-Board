from App.database import db
from datetime import date

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    listing_date = db.Column(db.Date, nullable=False)

    applications = db.relationship('Application', backref='listing', lazy=True, cascade="all, delete-orphan")

    def __init__(self, job_id, employer_id, listing_date):
        self.job_id = job_id
        self.employer_id = employer_id
        self.listing_date = listing_date or date.today()
        
    def __repr__(self):
        return f"<Listing(listing_id={self.id}, job_id={self.job_id}, employer_id={self.employer_id}, listing_date={self.listing_date})>"