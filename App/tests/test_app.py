import os, pytest, unittest, logging

from App.main import create_app
from App.database import db, create_db
from datetime import date

from App.controllers import (
    create_user,
    get_user_from_username,
    get_employer_jobs,
    authenticate,
    create_job,
    add_listing,
    get_listing,
    submit_application,
    get_applications_for_applicant,
    get_applications_for_job,
    set_application_status,
)

# Log errors
LOGGER = logging.getLogger(__name__)

# Setup app with a test database
app = create_app({"SQLALCHEMY_DATABASE_URI": 'sqlite:///test_database.db', "TESTING": True, "DEBUG": True})


'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_create_applicant(self):
        user = create_user("john_doe", "johndoe123", "applicant","John Doe")
        assert user.username == "john_doe"
        assert user.name == "John Doe"
        assert user.type == "applicant"
    
    def test_create_employer(self):
        user = create_user("spaceX", "spaceX123", "employer","Space X")
        assert user.username == "spaceX"
        assert user.company_name == "Space X"
        assert user.type == "employer"

    def test_create_job(self):
        job = create_job(2, "Software Developer", 60000.0, "Full-time role")
        assert job.title == "Software Developer"
        assert job.salary == 60000.0
        assert job.description == "Full-time role"
        assert job.employer_id == 2

    def test_create_listing(self):
        listing = add_listing(1, 2, date.today())
        assert listing.employer_id == 2
        assert listing.job_id == 1
        assert listing.listing_date == date.today()
    
    def test_submit_application(self):
        application = submit_application(1, 1, date.today())
        assert application.applicant_id == 1
        assert application.listing_id == 1
        assert application.submission_date == date.today()
        assert application.status == 'pending'

    def test_get_apps_by_applicant(self):
        applications = get_applications_for_applicant(1)
        assert len(applications) >= 0 # Ensure applications are returned
    
    
'''
    Integration Tests
'''

# Fixture for empty DB
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    create_db()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

def test_authenticate():
    # Create a user and test authentication
    user = create_user("john_doe", "johndoe123", "applicant","John Doe")
    token = authenticate("john_doe", "johndoe123")
    assert token is not None

def test_get_applications():
    # Test that an application created by user can be retrieved
    applicant = create_user("applicant1", "password", "applicant", "Applicant One")
    job = create_job(2, "Game Developer", 120000, "Full-time role")
    listing = add_listing(job.id, 2, date.today())
    submit_application(applicant_id=applicant.id, listing_id=listing.id)

    applications = get_applications_for_applicant(applicant.id)
    assert len(applications) > 0
    assert applications[0].applicant_id == applicant.id
    assert applications[0].listing_id == listing.id


def test_update_application_status():
    applicant = create_user("applicant2", "password", "applicant", "Applicant Two")
    listing = get_listing(2)
    application = submit_application(applicant_id=applicant.id, listing_id=listing.id)
    set_application_status(application.id, 'accepted')
    assert application.applicant_id == applicant.id
    assert application.listing_id == listing.id
    assert listing.employer_id == 2
    assert application.status == 'accepted'

def test_get_jobs_for_employer():
    employer = create_user("employer2", "password", "employer", "Employer Two")
    job = create_job(employer.id, "Music Engineer", 25000, "Designing sound effects")
    jobs = get_employer_jobs(employer.id)
    assert len(jobs) > 0
    assert jobs[0].id == job.id
    assert jobs[0].employer_id == employer.id
    assert jobs[0].title == "Music Engineer"
    assert jobs[0].salary == 25000
    assert jobs[0].description == "Designing sound effects"

def test_get_applications_for_job():
    listing = get_listing(2)
    applications = get_applications_for_job(listing.id)
    assert len(applications) > 0
    assert applications[0].listing_id == listing.id
    assert applications[0].applicant_id == get_user_from_username("applicant1").id
    