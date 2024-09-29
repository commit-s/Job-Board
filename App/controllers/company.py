from App.models import Company, Job
from App.database import db
from tabulate import tabulate

# View all companies
def view_all_companies():
    companies = Company.query.all()
    if not companies:
        return None
    table_data = []
    for company in companies:
        job_count = Job.query.filter_by(company_id=company.id).count()
        table_data.append([company.id, company.username, company.name, company.company_name, job_count])
    headers = ["Company ID", "Username", "Name", "Company Name", "Jobs"]
    return tabulate(table_data, headers, tablefmt="fancy_grid")
