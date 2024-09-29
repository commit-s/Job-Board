from App.models import Listing, Company, Job, Application
from tabulate import tabulate

# Get all listings
def get_all_listings():
    listings = Listing.query.all()
    if not listings:
        return None

    table_data = []
    headers = ["Listing ID", "Company", "Job", "Description", "Salary", "Date", "Applications"]
    for listing in listings:
        company = Company.query.get(listing.company_id)
        job = Job.query.get(listing.job_id)
        if not (company and job):
            continue

        application_count = Application.query.filter_by(listing_id=listing.listing_id).count()
        table_data.append([listing.listing_id, company.company_name, job.title, job.description, f'${job.salary:.2f}', listing.listing_date, application_count])

    return tabulate(table_data, headers, tablefmt="fancy_grid")

# Get all company listings
def get_company_listings(company_id):
    listings = Listing.query.filter_by(company_id=company_id).all()
    if not listings:
        return None

    table_data = []
    headers = ["Listing ID", "Company", "Job", "Description", "Salary", "Date", "Applications"]
    for listing in listings:
        company = Company.query.get(listing.company_id)
        job = Job.query.get(listing.job_id)
        if not (company and job):
            continue
        applicant_count = Application.query.filter_by(listing_id=listing.listing_id).count()
        table_data.append([listing.listing_id, company.company_name, job.title, job.description, f'${job.salary:.2f}', listing.listing_date, applicant_count])

    return tabulate(table_data, headers, tablefmt="fancy_grid")

# Get a specific listing
def get_listing(listing_id):
    return Listing.query.get(listing_id)
