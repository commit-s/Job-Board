from datetime import date, timedelta
import random

# Create notable companies
companies = [
    ("google", "securePassword1", "Google", "employer", "Google LLC"),
    ("meta", "securePassword2", "Meta", "employer", "Meta Platforms, Inc."),
    ("apple", "securePassword3", "Apple", "employer", "Apple Inc."),
    ("amazon", "securePassword4", "Amazon", "employer", "Amazon.com, Inc."),
    ("microsoft", "securePassword5", "Microsoft", "employer", "Microsoft Corporation"),
    ("tesla", "securePassword6", "Tesla", "employer", "Tesla, Inc."),
    ("netflix", "securePassword7", "Netflix", "employer", "Netflix, Inc."),
    ("twitter", "securePassword8", "Twitter", "employer", "Twitter, Inc."),
    ("linkedin", "securePassword9", "LinkedIn", "employer", "LinkedIn Corporation"),
    ("salesforce", "securePassword10", "Salesforce", "employer", "Salesforce.com, Inc.")
]

# Sample applicants
applicants = [
    ("john_doe", "password123", "John Doe"),
    ("jane_smith", "password456", "Jane Smith"),
    ("mike_johnson", "password789", "Mike Johnson"),
    ("lisa_white", "password101", "Lisa White"),
    ("paul_brown", "password102", "Paul Brown"),
    ("emma_jones", "password103", "Emma Jones"),
    ("james_black", "password104", "James Black"),
    ("olivia_green", "password105", "Olivia Green"),
    ("liam_gray", "password106", "Liam Gray"),
    ("sophia_wilson", "password107", "Sophia Wilson"),
    ("isabella_hall", "password108", "Isabella Hall"),
    ("mason_thompson", "password109", "Mason Thompson"),
    ("charlotte_lewis", "password110", "Charlotte Lewis"),
    ("noah_clark", "password111", "Noah Clark"),
    ("ava_rodriguez", "password112", "Ava Rodriguez"),
    ("elijah_martinez", "password113", "Elijah Martinez"),
    ("mia_anderson", "password114", "Mia Anderson"),
    ("lucas_taylor", "password115", "Lucas Taylor"),
    ("harper_jackson", "password116", "Harper Jackson"),
    ("jack_moore", "password117", "Jack Moore"),
    ("amelia_smith", "password118", "Amelia Smith"),
]


 # Sample jobs (20 jobs for testing)
jobs = [
    (1, "Software Engineer", 120000.0, "Develop and maintain software applications.", date(2024, 1, 1)),
    (1, "Data Scientist", 110000.0, "Analyze data and build predictive models.", date(2024, 1, 2)),
    (1, "Product Manager", 130000.0, "Lead product development initiatives.", date(2024, 1, 3)),
    (2, "Web Developer", 95000.0, "Build and maintain web applications.", date(2024, 1, 4)),
    (2, "UX Designer", 85000.0, "Design user experiences for web and mobile.", date(2024, 1, 5)),
    (2, "Marketing Specialist", 80000.0, "Develop marketing strategies and campaigns.", date(2024, 1, 6)),
    (3, "Sales Associate", 60000.0, "Assist customers and sell products.", date(2024, 1, 7)),
    (3, "Business Analyst", 90000.0, "Analyze business processes and suggest improvements.", date(2024, 1, 8)),
    (4, "Graphic Designer", 70000.0, "Create visual content for branding.", date(2024, 1, 9)),
    (5, "Network Engineer", 100000.0, "Manage and support network systems.", date(2024, 1, 10)),
    (6, "Customer Support Representative", 50000.0, "Provide support to customers.", date(2024, 1, 11)),
    (7, "Project Coordinator", 75000.0, "Assist in project management activities.", date(2024, 1, 12)),
    (8, "Quality Assurance Tester", 80000.0, "Ensure the quality of software products.", date(2024, 1, 13)),
    (9, "Database Administrator", 95000.0, "Manage and maintain database systems.", date(2024, 1, 14)),
    (10, "System Analyst", 90000.0, "Analyze system requirements and design solutions.", date(2024, 1, 15)),
    (1, "DevOps Engineer", 115000.0, "Automate deployment processes.", date(2024, 1, 16)),
    (2, "SEO Specialist", 70000.0, "Optimize websites for search engines.", date(2024, 1, 17)),
    (3, "Content Writer", 60000.0, "Write engaging content for websites and blogs.", date(2024, 1, 18)),
    (4, "Mobile App Developer", 100000.0, "Create applications for mobile devices.", date(2024, 1, 19)),
    (5, "Technical Writer", 80000.0, "Write technical documentation for products.", date(2024, 1, 20))
]


# Sample applications (generated randomly)
def generate_applications(num_applicants=20, num_listings=20, total_applications=100):
    applications = []
    statuses = ["pending", "accepted", "rejected"]
    applicant_ids = list(range(11, 11 + num_applicants))
    listing_ids = list(range(1, 1 + num_listings))
    
    # Ensure each listing gets at least one application
    for listing_id in listing_ids:
        applicant_id = random.choice(applicant_ids)
        submission_date = date.today() - timedelta(days=random.randint(0, 30))
        status = random.choice(statuses)
        applications.append((applicant_id, listing_id, submission_date, status))

    # Fill the rest of the applications
    while len(applications) < total_applications:
        applicant_id = random.choice(applicant_ids)
        listing_id = random.choice(listing_ids)
        submission_date = date.today() - timedelta(days=random.randint(0, 30))
        status = random.choice(statuses)

        # Ensure the applicant has not already applied to the same job
        if (applicant_id, listing_id) not in [(app[0], app[1]) for app in applications]:
            applications.append((applicant_id, listing_id, submission_date, status))

    return applications

# Generate the applications table
applications = generate_applications(total_applications=100)