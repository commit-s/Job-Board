from App.models import User, Employer, Applicant, Application
from App.database import db
from sqlalchemy.exc import SQLAlchemyError


def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

# Get all employers
def get_all_employers():
    return Employer.query.all()

# Get all applicants
def get_all_applicants():
    return Applicant.query.all()

# Get all applications for a specified applicant
def get_applications_for_applicant(applicant_id):
    return Application.query.filter_by(applicant_id=applicant_id).all()

# Creates a new user of a given user_type
def create_user(username, password, user_type='applicant', name=None):
    if user_type == 'employer':
        newuser = Employer(username=username, password=password, company_name=name)
    elif user_type == 'applicant':
        newuser = Applicant(username=username, password=password, name=name)
    else:
        raise ValueError("Invalid user type")
    
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error creating user: {e}')
    return None

# Updates a user given id and optional username and name
def update_user(id, username=None, name=None):
    user = get_user(id)
    if not user:
        return None
    
    if username is not None:
        user.username = username
    if name is not None:
        user.name = name

    db.session.commit()
    return user

# Deletes a user from the database
def delete_user(id):
    user = get_user(id)
    if not user:
        return None
    
    db.session.delete(user)
    db.session.commit()
    return user


