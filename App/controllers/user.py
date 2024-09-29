from App.models import User, Company, Applicant
from tabulate import tabulate
from App.database import db

def create_user(username, password, name, user_type, company_name=None):
    if user_type == 'company':
        newuser = Company(username=username, password=password, name=name, company_name=company_name)
    elif user_type == 'applicant':
        newuser = Applicant(username=username, password=password, name=name)
    else:
        raise ValueError("Invalid user type")
    
    db.session.add(newuser)
    db.session.commit()
    
    db.session.add(newuser)
    db.session.commit()
    return newuser

def delete_user(id):
    user = get_user(id)
    if not user:
        return None
    db.session.delete(user)
    db.session.commit()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_table():
    users = User.query.all()
    table_data = [[user.id, user.username, user.name, user.type] for user in users]
    headers = ["User ID", "Username", "Name", "Type"]
    return tabulate(table_data, headers, tablefmt="fancy_grid")

def update_user(id, username=None, name=None):
    user = get_user(id)
    if not user:
        return None
    
    if not username is None:
        user.username = username
    if not name is None:
        user.name = name

    db.session.add(user)
    return db.session.commit()