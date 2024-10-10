# views/listings.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from App.controllers import (
    get_user,
    get_job,
    add_listing,
    remove_listing,
    get_listing,
    get_all_listings,
    get_employer_listings,
)


listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

# Create a listing
@listing_views.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
    data = request.json
    job_id = data.get('jobID')
    listing_date = data.get('listingDate')

    if not job_id:
        return jsonify({'error':'jobID and listingDate are required fields!'}), 400
    
    if listing_date:
        try:
            listing_date = datetime.strptime(listing_date, '%d-%m-%Y').date() # Convert string to a datetime object
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use DD-MM-YYYY.'}), 400

    current_user = get_jwt_identity() # gives username
    employer = get_user(current_user)

    if not employer or employer.type != 'employer': # ensure user is an employer
        return jsonify({'error': 'Only employers can create listings!'}), 403
    
    job = get_job(job_id)
    if not job: # ensure job exists in the database
        return jsonify({'error':f'Job with id {job_id} not found!'}), 404
    
    if employer.id != job.employer_id:
        return jsonify({'error':'Unauthorized action'}), 403
    
    # create the listing
    listing = add_listing(job.id, employer.id, listing_date)
    if not listing:
        return jsonify({'error': f'Failed to add job {job.id} to listing'}), 500
    
    if isinstance(listing, int):
        return jsonify({'error':f'Listing for job {job.id} already exists', 'listingID': listing}), 400
    
    return jsonify({'message': f'Listing for job {job_id} added successfully!', 'listingID': listing.id}), 201


# Get listings
@listing_views.route('/listings', methods=['GET'])
def get_listings():
    employer_id = request.args.get('employer')

    # Get listings for the specific employer
    if employer_id:
        listings = get_employer_listings(employer_id)
        if not listings:
            return jsonify({'error':f'No listings found for employer {employer_id}'}), 404
    else:
        listings = get_all_listings()
    
    result = []
    for listing in listings:
        job = listing.job
        result.append({
            'listingID': listing.id,
            'employerID': listing.employer_id,
            'listingDate': listing.listing_date,
            'applicants': len(listing.applications),
            'job': {
                'jobID': job.id,
                'title': job.title,
                'salary': job.salary,
                'description': job.description,
                'employerID': job.employer_id
            }
        })
    return jsonify(result), 200
    

# Delete a listing
@listing_views.route('/listings/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    listing = get_listing(listing_id)

    if not listing:
        return jsonify({'error': f'Listing {listing_id} does not exist'}), 404
    
    current_user = get_jwt_identity()
    employer = get_user(current_user)

    if not employer or employer.type != 'employer' or employer.id != listing.employer_id:
        return jsonify({'error': 'Only employers can delete their listings!'}), 403
    
    if remove_listing(listing_id) is None:
        return jsonify({'error':f'Error unlisting listing {listing_id}'}), 500
    
    return jsonify({'message':f'Listing {listing_id} for job {listing.job_id} was unlisted'}), 200
    
