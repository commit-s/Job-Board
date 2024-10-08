from App.database import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Double)
    description = db.Column(db.Text)
    
    listings = db.relationship('Listing', backref='job', lazy=True, cascade='all, delete-orphan')

    def __init__(self, employer_id, title, salary, description):
        self.employer_id = employer_id
        self.title = title
        self.salary = salary
        self.description = description

        
    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, salary=${self.salary:.2f}, description={self.description})>"