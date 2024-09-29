from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,  # Polymorphic behavior based on 'type'
        'polymorphic_identity': 'user'
    }

    def __init__(self, username, password, name):
        self.username = username
        self.name = name
        self.set_password(password)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, name={self.name}, type={self.type})>"

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

