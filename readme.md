
Here's a structured documentation for your commands, suitable for inclusion in your README.txt file for your GitHub repository. This documentation outlines the functionality of each command, including their purpose, arguments, and options.

# Command Line Interface Documentation
This document provides an overview of the command line interface (CLI) commands implemented in the application.

## Initialization Command
### init
Description: Creates and initializes the database.
Usage:
```bash
$   flask init
```

## User Commands
User Group: user

### create
Description: Creates a user (applicant or company).
Arguments:
-username: The username for the user.
-password: The password for the user.
-name: The full name of the user.
Prompt: Enter user type (applicant/company).
Usage:
```bash
$   flask user create <username> <password> <name>
```

### delete
Description: Deletes a user from the database.
Arguments:
-id: The ID of the user to be deleted.
Usage:
```bash
$   flask user delete
$   Enter the user id: <id>
```

### update
Description: Updates a user's username or name in the database.
Arguments:
-id: The ID of the user to update.
Options:
--username: New username (optional).
--name: New name (optional).
Usage:
```bash
$   flask user update <id> [--username <new_username>] [--name <new_name>]
```

### view-all
Description: Lists all users in the database.
Usage:
```bash
$   flask user view-all
```

### view-companies
Description: Lists all companies in the database.
Usage:
```bash
$   flask user view-companies
```

### view-applicants
Description: Lists all applicants in the database.
Usage:
```bash
$   flask user view-applicants
```

### view-jobs
Description: View all job listings posted by a specified company.
Arguments:
-company_id: The ID of the company.
Usage:
```bash
$   flask user view-jobs
$   Enter company id: <company_id>
```

### view-applications
Description: View all applications for a specified applicant.
Arguments:
-applicant_id: The ID of the applicant.
Usage:
```bash
$   flask user view-applications <applicant_id>
$   Enter applicant id: <applicant_id>
```

## Job and Application Commands
Job Group: job

### create
Description: Creates a job listing for a specified company.
Arguments:
-company_id: The ID of the company creating the job listing.
-title: The title of the job listing.
Options:
--salary: Salary for the job (default is 0.0).
--description: Job description (default is empty).
Usage:
```bash
$   flask job create <company_id> <title> [--salary <salary>] [--description <description>]
```

### delete
Description: Deletes a job listing from a company.
Arguments:
-job_id: The ID of the job to be deleted.
Usage:
```bash
$   flask job delete <job_id>
```

### update
Description: Updates a job listing.
Arguments:
-job_id: The ID of the job to update.
Options:
--title: New title for the job (optional).
--salary: New salary for the job (optional).
--description: New description for the job (optional).
Usage:
```bash
$   flask job update <job_id> [--title <new_title>] [--salary <new_salary>] [--description <new_description>]
```

### view-all
Description: View all job listings.
Usage:
```bash
$ flask job view-all
```

### view-applications
Description: View all applicants for a specified job listing.
Arguments:
-listing_id: The ID of the job listing.
Usage:
```bash
$   flask job view-applications
$   Enter listing id: <listing_id>
```

### submit-application
Description: Submit an application for a specified job listing.
Arguments:
-listing_id: The ID of the job listing.
-applicant_id: The ID of the applicant submitting the application.
Usage:
```bash
$   flask job submit-application
$   Enter the listing id: <listing_id>
$   Enter the applicant id: <applicant_id>
```

### delete-application
Description: Deletes a specific application given its ID.
Arguments:
-application_id: The ID of the application to be deleted.
-applicant_id: The ID of the applicant who submitted the application.
Usage:
```bash
$   flask job delete-application
$   Enter the applicant id: <applicant_id>
$   Enter the application id: <application_id>
```

### update-application-status
Description: Updates the status of a specific application for a job.
Usage:
```bash
$   flask job update-application-status
$   Enter company id: <company_id>
$   Enter listing id: <listing_id>
$   Enter applicatio id: <application_id>
$   Enter application status (pending/accepted/rejected): [pending]
```