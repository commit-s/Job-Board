from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    get_user,
    get_listing,
    submit_application,
    get_application,
    set_application_status,
    get_applications_for_job,
    get_applications_for_applicant
)

application_views = Blueprint('application_views', __name__, template_folder='../templates')

# Apply to a job listing
@application_views.route('/listings/<int:listing_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_listing(listing_id):
    current_user = get_jwt_identity()
    applicant = get_user(current_user)

    if not applicant or applicant.type != 'applicant':
        return jsonify({'error': 'not authenticated'}), 401
    
    listing = get_listing(listing_id)
    if not listing:
        return jsonify({'error':f'listing id {listing_id} not found'}), 404

    application, status = submit_application(applicant.id, listing_id) # empty listing date = date.today()
    if not applicant:
        return jsonify({'error': 'Application submission failed'}), 500
    
    if status == 1:
        return jsonify({'error': 'Application already submitted', 'applicationID': application.id}), 400
    
    return jsonify({'message': 'Application submitted', 'applicationID': application.id}), 201


# List applications/applicants for a specific job listing
@application_views.route('/listings/<int:listing_id>/applicants', methods=['GET'])
@jwt_required()
def get_applicants_for_listing(listing_id):
    current_user = get_jwt_identity()
    employer = get_user(current_user)
    listing = get_listing(listing_id)

    print(f'listing id {listing_id}, employer {current_user}')
    if not employer or employer.type != 'employer': # verify that user is an employer
        return jsonify({'error': 'not authenticated'}), 401
    
    if not listing:
        return jsonify({'error':'listing does not exist'}), 404
    
    # verify that listing belongs to employer
    if employer.id != listing.employer_id:
        return jsonify({'error':'Unauthorized action'}), 403
    
    applications = get_applications_for_job(listing_id)
    if not applications:
        return jsonify({'error':f'no applications found for listing {listing_id}'}), 404
    
    applicants = [
        {
            'applicationID': application.id,
            'listingID': application.listing_id,
            'status': application.status,
            'submissionDate': application.submission_date,
            'applicant': {
                'applicantID': application.applicant.id,
                'name': application.applicant.name
            }
        } for application in applications
    ]
    return jsonify({'message':'Applicants received', 'applicants':applicants}), 200


# Update an application status
@application_views.route('/applications/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application_status(application_id):
    current_user = get_jwt_identity()
    employer = get_user(current_user)
    application = get_application(application_id)

    if not employer or employer.type != 'employer':
        return jsonify({'error': 'not authenticated'}), 401

    if not application:
        return jsonify({'error':f'application id {application_id} not found'}), 404
    
    # Ensure that the employer is the owner of the job listing the application belongs to
    if employer.id != application.listing.employer_id:
        return jsonify({'error':'Unauthorized action'}), 403
        
    data = request.json
    new_status = data.get('status')

    if new_status not in ['pending', 'accepted', 'rejected']:
        return jsonify({'error':'Invalid status value'}), 400
    
    set_application_status(application_id, new_status)
    return jsonify({'message': 'status updated', 'applicationID':application_id, 'status':new_status}), 201


# Get applications from a specific applicant
@application_views.route('/applications/<int:applicant_id>', methods=['GET'])
@jwt_required()
def get_applications_by_applicant(applicant_id):
    current_user = get_jwt_identity()
    applicant = get_user(current_user)

    if not applicant or applicant.type != 'applicant':
        return jsonify({'error': 'not authenticated'}), 401

    if current_user != applicant_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    
    applications = get_applications_for_applicant(applicant_id)
    if not applications:
        return jsonify({"message": "No applications found"}), 404
    
    applications_list = [
        {
            'applicationID': application.id,
            'listingID': application.listing_id,
            'status': application.status,
            'submissionDate': application.submission_date,
            'job': {
                'jobID': application.listing.job.id,
                'title': application.listing.job.title,
                'salary': application.listing.job.salary,
                'description': application.listing.job.description,
            }
        } for application in applications
    ]

    return jsonify({'message':'Applications retrieved', 'applications': applications_list}), 200