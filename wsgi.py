import click
from flask import Flask
from flask.cli import AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (
    initialize, create_user, delete_user, update_user,get_all_users, get_all_employers, get_all_applicants, get_employer_jobs,
    get_applications_for_applicant, create_job, get_all_listings, get_applications_for_job, submit_application
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
@click.argument("username",type=str)
@click.argument("password")
def create_user_command(username, password, name):
    user_type = click.prompt("Enter user type (applicant/employer)", 
                              type=click.Choice(['applicant', 'employer'], case_sensitive=False), 
                              default="applicant")
    name=None
    if user_type == 'employer':
        name = click.prompt("Enter company name", type=str)
    elif user_type == 'applicant':
        name = click.prompt("Enter Name", type=str)
    create_user(username, password, user_type, name)
    print(f'{user_type.capitalize()} "{username}" created!')

@user_cli.command("delete", help="Deletes a user in the database")
@click.argument("user_id", type=int)
def delete_user_command():
    user_id = click.prompt("Enter the user id", type=int)
    delete_user(user_id)
    print(f'User {user_id} deleted!')


@user_cli.command("update", help="Updates a user's username or name in the database")
@click.argument("id")
@click.option("--username", default=None)
@click.option("--name", default=None)
def update_user_command(id, username, name):
    update_user(id, username, name)
    print(f'User {id} updated!')

@user_cli.command("get-all", help="Lists all users in the database")
def view_all_users_command():
    print(get_all_users())

@user_cli.command("get-employers", help="Lists all employers in the database")
def view_all_companies_command():
    print(get_all_employers())

@user_cli.command("get-applicants", help="Lists all applicants in the database")
def view_all_applicants_command():
    print(get_all_applicants())

@user_cli.command("get-jobs", help="View all job listings posted by an employer")
@click.argument("employer_id", type=int)
def view_company_jobs_command(employer_id):
    print(get_employer_jobs(employer_id))

@user_cli.command("get-applications", help="View all applications for an applicant")
@click.argument("applicant_id", type=int)
def view_applicant_applications_command(applicant_id):
    print(get_applications_for_applicant(applicant_id))

app.cli.add_command(user_cli)

# Job and Application Commands
job_cli = AppGroup('job', help='Job listing commands')

@job_cli.command('create', help="Creates a job listing for a company")
@click.argument("company_id")
@click.argument("title")
@click.option("--salary", default=0.0)
@click.option("--description", default="")
def create_job_command(employer_id, title, salary, description):
    create_job(employer_id, title, salary, description)
    print(f'Job "{title}" created for employer "{employer_id}"')


@job_cli.command('get-all', help="View all job listings")
def view_job_listings_command():
    print(get_all_listings())

@job_cli.command('get-applications', help='View all applicants for a job listing')
@click.argument("listing_id", type=int)
def view_applicants_for_job_command(listing_id):
    print(get_applications_for_job(listing_id))

@job_cli.command('submit-application', help="Submit an application for a job")
@click.argument('applicant_id', type=int)
@click.argument('listing_id', type=int)
def submit_application_command(applicant_id, listing_id):
    submit_application(applicant_id, listing_id)
    print(f"Application for listing {listing_id} submitted by applicant {applicant_id}.")

app.cli.add_command(job_cli)
