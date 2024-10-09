from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from App.models import User

from App.controllers import (
    create_user,
    get_user_from_username,
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

# Sign up to 'JOBIFY' with a username, password, usertype and a name/company_name
@auth_views.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'username already taken!'}), 400
    
    create_user(data['username'], data['password'], data['user_type'], data['name'])
    return jsonify({'message': 'account created'}), 201

# log into account with username and password, generate a token for the session
@auth_views.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    user = get_user_from_username(username)

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=username)
        return jsonify({'token':access_token, 'id':user.id}), 200
    
    return jsonify({'error':'invalid credentials!'}), 400


