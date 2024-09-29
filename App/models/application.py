from App.database import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='status_enum'), default='pending')
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.listing_id'))
    submission_date = db.Column(db.Date, nullable=False)
        
    def view_status(self):
        return self.status
    
    def __repr__(self):
        return f"<Application(id={self.id}, status={self.status})>"