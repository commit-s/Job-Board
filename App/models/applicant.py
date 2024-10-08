from App.database import db
from App.models.user import User

class Applicant(User):
    __tablename__ = 'applicant'  # Separate table for applicants
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True) # To reference Applicant as a foreign key
    name = db.Column(db.String(50), nullable=False)
    
    applications = db.relationship('Application', backref='applicant', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'applicant'  # Identify this class as 'applicant'
    }

    def __init__(self, username, password, name):
        super().__init__(username, password)
        self.type = 'applicant'
        self.name = name
        
    def __repr__(self):
        return f"<Applicant(id={self.id}, username={self.username}, name={self.name})>"