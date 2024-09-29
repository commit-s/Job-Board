import click
from flask import Flask
from flask.cli import AppGroup

from App.database import db, get_migrate
from App.models import Company, Applicant, Listing, Job
from App.main import create_app
from App.controllers import (
    create_user, update_user, delete_user, get_all_users_table, initialize,
    create_job, delete_job, update_job, view_all_companies, view_all_applicants,
    get_all_listings, get_company_listings, submit_application, delete_application,
    update_application_status, get_applications_for_applicant, view_applications_for_job
)

# Function to center a title based on table width
def center_title(title, table):
    table_lines = table.split('\n')
    max_line_length = max(len(line) for line in table_lines)
    title_length = len(title)

    if title_length < max_line_length:
        padding = (max_line_length - title_length) // 2
        return ' ' * padding + title
    return title

# Initialize the application and database migration
app = create_app()
migrate = get_migrate(app)

# Command to create and initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Database initialized')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username")
@click.argument("password")
@click.argument("name")
def create_user_command(username, password, name):
    user_type = click.prompt("Enter user type (applicant/company)", 
                              type=click.Choice(['applicant', 'company'], case_sensitive=False), 
                              default="applicant")
    
    if user_type == 'company':
        company_name = click.prompt("Enter company name", type=str)
        create_user(username, password, name, user_type, company_name=company_name)
    else:
        create_user(username, password, name, 'applicant')
    
    print(f'{user_type.capitalize()} "{username}" created!')

@user_cli.command("delete", help="Deletes a user in the database")
@click.argument("id")
def delete_user_command(id):
    delete_user(id)
    print(f'User {id} deleted!')

@user_cli.command("update", help="Updates a user's username or name in the database")
@click.argument("id")
@click.option("--username", default=None)
@click.option("--name", default=None)
def update_user_command(id, username, name):
    update_user(id, username, name)
    print(f'User {id} updated!')

@user_cli.command("view-all", help="Lists all users in the database")
def view_all_users_command():
    user_table = get_all_users_table()
    if user_table:
        print(center_title("Users", user_table))
        print(user_table)

@user_cli.command("view-companies", help="Lists all companies in the database")
def view_all_companies_command():
    company_table = view_all_companies()
    if company_table:
        print(center_title("Companies", company_table))
        print(company_table)

@user_cli.command("view-applicants", help="Lists all applicants in the database")
def view_all_applicants_command():
    applicant_table = view_all_applicants()
    if applicant_table:
        print(center_title("Applicants", applicant_table))
        print(applicant_table)

@user_cli.command("view-jobs", help="View all job listings posted by a company")
@click.argument("company_id")
def view_company_jobs_command(company_id):
    jobs = get_company_listings(company_id)
    if jobs:
        company_name = Company.query.get(company_id).company_name
        print(center_title(f"Jobs from Company '{company_name}'", jobs))
        print(jobs)
    else:
        print(f"No jobs found for company ID: {company_id}")

@user_cli.command("view-applications", help="View all applications for an applicant")
@click.argument("applicant_id")
def view_applicant_applications_command(applicant_id):
    applications = get_applications_for_applicant(applicant_id)
    if applications:
        applicant_name = Applicant.query.get(applicant_id).username
        print(center_title(f"Applications from Applicant '{applicant_name}'", applications))
        print(applications)
    else:
        print(f"No applications found for applicant ID: {applicant_id}")

app.cli.add_command(user_cli)

'''
Job and Application Commands
'''
job_cli = AppGroup('job', help='Job listing commands')

@job_cli.command('create', help="Creates a job listing for a company")
@click.argument("company_id")
@click.argument("title")
@click.option("--salary", default=0.0)
@click.option("--description", default="")
def create_job_command(company_id, title, salary, description):
    job = create_job(company_id, title, salary, description)
    if job is None:
        print("Invalid COMPANY_ID, Job not created!")
    else:
        print(f'Job "{title}" created for company "{company_id}"')

@job_cli.command('delete', help="Deletes a job listing from the company")
@click.argument("job_id")
def delete_job_command(job_id):
    deleted = delete_job(job_id)
    if deleted is None:
        print(f'Job {job_id} not found!')
    else:
        print(f'Job "{job_id}" deleted.')

@job_cli.command('update', help="Updates a job listing")
@click.argument("job_id")
@click.option("--title", default=None)
@click.option("--salary", default=None)
@click.option("--description", default=None)
def update_job_command(job_id, title, salary, description):
    job = update_job(job_id, title, salary, description)
    if job is None:
        print(f'Job {job_id} not found!')
    else:
        print(f'Job "{job_id}" updated.')

@job_cli.command('view-all', help="View all job listings")
def view_job_listings_command():
    jobs = get_all_listings()
    if jobs:
        print(center_title("Jobs", jobs))
        print(jobs)
    else:
        print("No job listings found.")

@job_cli.command('view-applications', help='View all applicants for a job listing')
@click.argument("listing_id")
def view_applicants_for_job_command(listing_id):
    applications = view_applications_for_job(listing_id)
    if applications:
        listing = Listing.query.get(listing_id)
        company_name = Company.query.get(listing.company_id).company_name
        job_title = Job.query.get(listing.job_id).title
        print(center_title(f"Applications for Job '{job_title}' by '{company_name}'", applications))
    print(applications)

@job_cli.command('submit-application', help="Submit an application for a job")
@click.argument("listing_id")
@click.argument("applicant_id")
def submit_application_command(listing_id, applicant_id):
    application = submit_application(applicant_id, listing_id)
    if application == 1:
        print(f"Applicant ID: '{applicant_id}' is INVALID!")
    elif application == 2:
        print(f"Listing ID: '{listing_id}' is INVALID!")
    elif application == 3:
        print(f"Applicant ID: '{applicant_id}' has already applied for Listing ID: '{listing_id}'!")
    else:
        print(f"Application for listing {listing_id} submitted by applicant {applicant_id}.")

@job_cli.command('delete-application', help="Delete an application given its ID")
@click.argument("application_id")
@click.argument("applicant_id")
def delete_application_command(application_id, applicant_id):
    deleted = delete_application(applicant_id, application_id)
    if deleted is None:
        print('Invalid Permissions: Application does not belong to Applicant!')
    else:
        print(f'Deleted Application {application_id} for Applicant {applicant_id}')

@job_cli.command('update-application-status', help="Update the status of an application for a job")
def change_application_status_command():
    company_table = view_all_companies()
    if company_table:
        print(center_title("Companies", company_table))
        print(company_table)
    company_id = click.prompt("Enter company id", type=int)
    
    jobs = get_company_listings(company_id)
    if jobs:
        company_name = Company.query.get(company_id).company_name
        print(center_title(f"Jobs from Company '{company_name}'", jobs))
        print(jobs)
    listing_id = click.prompt("Enter listing id", type=int) 

    applications = view_applications_for_job(listing_id)
    if applications:
        listing = Listing.query.get(listing_id)
        company_name = Company.query.get(listing.company_id).company_name
        job_title = Job.query.get(listing.job_id).title
        print(center_title(f"Applications for Job '{job_title}' by '{company_name}'", applications))
    print(applications)
    
    application_id = click.prompt("Enter application id", type=int)
    new_status = click.prompt("Enter application status (pending/accepted/rejected)", 
                              type=click.Choice(['pending', 'accepted', 'rejected'], case_sensitive=False), 
                              default="pending")
    
    if update_application_status(application_id, new_status):
        print(f"Application {application_id} status updated to '{new_status}'.")
    else:
        print(f"Failed to update status for application {application_id}.")

app.cli.add_command(job_cli)
