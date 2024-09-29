from App.database import db

class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    listing_date = db.Column(db.Date, nullable=False)
    applications = db.relationship('Application', backref='listing', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Listing(listing_id={self.listing_id}, job_id={self.job_id}, company_id={self.company_id}, listing_date={self.listing_date})>"