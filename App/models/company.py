from App.database import db
from App.models.user import User
from App.models.listing import Listing

class Company(User):
    __tablename__ = 'company'  # Separate table for companies
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_listings = db.relationship('Listing', backref='company', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'company'  # Identify this class as 'company'
    }

    def __init__(self, username, password, name, company_name):
        super().__init__(username, password, name)
        self.company_name = company_name

    def list_job(self, job):
        listing = Listing(company_id=self.id, job_id=job.id)
        db.session.add(listing)
        db.session.commit()

    def unlist_job(self, listing):
        db.session.delete(listing)
        db.session.commit()

    def __repr__(self):
        return f"<Company(id={self.id}, username={self.username}, company_name={self.company_name})>"