from App.database import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Double, nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    listings = db.relationship('Listing', backref='job', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, salary=${self.salary:.2f}, description={self.description})>"