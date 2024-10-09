# views/listings.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    get_user,
    create_job
)


job_views = Blueprint('job_views', __name__, template_folder='../templates')


# Create a Job
@job_views.route('/job', methods=['POST'])
@jwt_required()
def create_new_job():
    data = request.json
    current_user = get_jwt_identity()
    employer = get_user(current_user)

    if not employer or employer.type != 'employer':
        return jsonify({'error': 'Only employers can create jobs!'}), 403
    
    title = data.get('title')
    if not title:
        return jsonify({'error':'title not provided'}), 400
    
    job, status = create_job(employer.id, title, data['salary'], data['description'])
    if not job:
        return jsonify({'error': f'Failed to create job "{title}"'}), 500
    
    if status == 1:
        return jsonify({'error':f'job "{title}" already exists', 'jobID': job.id}), 400
    
    return jsonify({'message': f'Job created successfully!', 'job':job.id}), 201