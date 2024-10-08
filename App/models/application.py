from App.database import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='status_enum'), default='pending', nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    submission_date = db.Column(db.Date, nullable=False)
        
    
    def __init__(self, applicant_id, listing_id, submission_date, status):
        self.applicant_id = applicant_id
        self.listing_id = listing_id
        self.submission_date = submission_date
        self.status = status
    
    def __repr__(self):
        return f"<Application(id={self.id}, status={self.status}, applicant_id={self.applicant_id}, listing_id={self.listing_id})>"
    
    def view_status(self):
        return self.status