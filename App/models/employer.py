from App.database import db
from App.models.user import User

class Employer(User):
    __tablename__ = 'employer'  # Separate table for companies
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    
    job_listings = db.relationship('Listing', backref='company', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'employer'  # Identify this class as 'company'
    }

    def __init__(self, username, password, company_name):
        super().__init__(username, password)
        self.type = 'employer'
        self.company_name = company_name

    def __repr__(self):
        return f"<Company(id={self.id}, username={self.username}, company_name={self.company_name})>"