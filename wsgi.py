import click
from flask import Flask
from flask.cli import AppGroup

from App.database import db, get_migrate
from App.models import Company, Applicant, Listing, Job
from App.main import create_app
from App.controllers import (
    create_user, update_user, delete_user, get_all_users_table, initialize,
    create_job, delete_job, update_job, view_all_companies, view_all_applicants,
    get_all_listings, submit_application, delete_application,
    update_application_status, get_applications_for_applicant, view_applications_for_job,
)

from helpers import (
    display_all_users,
    display_all_companies,
    display_all_applicants,
    display_available_applicants,
    display_all_jobs,
    display_company_jobs,
    display_all_applicants_for_job,
    center_title
)

app = create_app()
migrate = get_migrate(app)

# Command to create and initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Database initialized')

# User Commands
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username")
@click.argument("password")
@click.argument("name")
def create_user_command(username, password, name):
    user_type = click.prompt("Enter user type (applicant/company)", 
                              type=click.Choice(['applicant', 'company'], case_sensitive=False), 
                              default="applicant")
    
    company_name = click.prompt("Enter company name", type=str) if user_type == 'company' else None
    create_user(username, password, name, user_type, company_name=company_name)

    print(f'{user_type.capitalize()} "{username}" created!')

@user_cli.command("delete", help="Deletes a user in the database")
def delete_user_command():
    display_all_users()
    user_id = click.prompt("Enter the user id", type=int)
    if delete_user(user_id):
        print(f'User {user_id} deleted!')
    else:
        print(f'Error deleting User {user_id}!')

@user_cli.command("update", help="Updates a user's username or name in the database")
@click.argument("id")
@click.option("--username", default=None)
@click.option("--name", default=None)
def update_user_command(id, username, name):
    if update_user(id, username, name):
        print(f'User {id} updated!')
    else:
        print(f'Error updating User {id}!')

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
def view_company_jobs_command():
    display_all_companies()
    company_id = click.prompt("Enter the company id", type=int)
    display_company_jobs(company_id)

@user_cli.command("view-applications", help="View all applications for an applicant")
def view_applicant_applications_command():
    display_all_applicants()
    applicant_id = click.prompt("Enter the applicant id", type=int)
    applications = get_applications_for_applicant(applicant_id)
    
    if applications:
        applicant_name = Applicant.query.get(applicant_id).name
        print(center_title(f"Applications from Applicant '{applicant_name}'", applications))
        print(applications)
    else:
        print(f"No applications found for applicant ID: {applicant_id}")

app.cli.add_command(user_cli)

# Job and Application Commands
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
def delete_job_command():
    display_all_jobs()
    job_id = click.prompt("Enter the job id", type=int)
    if delete_job(job_id) is None:
        print(f'Job {job_id} not found!')
    else:
        print(f'Job "{job_id}" deleted.')

@job_cli.command('update', help="Updates a job listing")
@click.argument("job_id")
@click.option("--title", default=None)
@click.option("--salary", type=float, default=None)
@click.option("--description", default=None)
def update_job_command(job_id, title, salary, description):
    if update_job(job_id, title, salary, description) is None:
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
def view_applicants_for_job_command():
    display_all_jobs()
    listing_id = click.prompt("Enter listing id", type=int)
    display_all_applicants_for_job(listing_id)

@job_cli.command('submit-application', help="Submit an application for a job")
def submit_application_command():
    display_all_jobs()
    listing_id = click.prompt("Enter the listing id", type=int)
    
    display_available_applicants(listing_id)
    
    applicant_id = click.prompt("Enter the applicant id", type=int)
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
def delete_application_command():
    display_all_applicants()
    applicant_id = click.prompt("Enter the applicant id", type=int)
    
    applications = get_applications_for_applicant(applicant_id)
    if applications:
        applicant_name = Applicant.query.get(applicant_id).username
        print(center_title(f"Applications from Applicant '{applicant_name}'", applications))
        print(applications)
    
    application_id = click.prompt("Enter application id", type=int)
    if delete_application(applicant_id, application_id) is None:
        print('Invalid Permissions: Application does not belong to Applicant!')
    else:
        print(f'Deleted Application {application_id} for Applicant {applicant_id}')

@job_cli.command('update-application-status', help="Update the status of an application for a job")
def update_application_status_command():
    display_all_companies()
    company_id = click.prompt("Enter company id", type=int)
    display_company_jobs(company_id)
    listing_id = click.prompt("Enter listing id", type=int) 
    display_all_applicants_for_job(listing_id)
    application_id = click.prompt("Enter application id", type=int)
    new_status = click.prompt("Enter application status (pending/accepted/rejected)", 
                              type=click.Choice(['pending', 'accepted', 'rejected'], case_sensitive=False), 
                              default="pending")
    
    if update_application_status(application_id, new_status):
        print(f"Application {application_id} status updated to '{new_status}'.")
        display_all_applicants_for_job(listing_id)
    else:
        print(f"Failed to update status for application {application_id}.")

app.cli.add_command(job_cli)
