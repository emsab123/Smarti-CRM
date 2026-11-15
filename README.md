# Smarti CRM – Customer and Job Management System

## 1. Project Overview

Smarti CRM is a simple web-based Customer Relationship Management (CRM) application developed as part of a technical assessment for Smarti Environmental Limited.

The application helps a business manage customer records, onboarding progress, appointments, fitters and maintenance engineers, and job statuses.

The aim was to develop a straightforward system that demonstrates how business information can be created, stored, retrieved and updated.

## 2. Features

### Customer Management
- Add customers with their name, email, phone number and address.
- View existing customer records.
- Edit customer information.
- Track onboarding progress.

### Customer Onboarding
- Assign onboarding statuses: New Enquiry, In Progress and Active.
- Update customer statuses as they progress.

### Appointments and Job Management
- Create appointments for existing customers.
- Assign appointment dates, times and staff members.
- View job records.
- Update job statuses, including Pending, In Progress and Completed.

### Staff Management
- Add fitters and maintenance engineers.
- View registered staff members.
- Delete staff records.
- Prevent deletion of staff members assigned to existing jobs.

## 3. Technologies Used

- **Python:** Main programming language.
- **Streamlit:** Used to develop the web-based interface.
- **SQLite:** Local relational database for storing application data.
- **Pandas:** Used to display database records in tables.
- **Git:** Version control.

## 4. Project Structure

- `app.py` – Main application and user interface.
- `database.py` – Database operations and data management.
- `smarti.db` – Local SQLite database, automatically created when the application first runs.
- `requirements.txt` – Python dependencies.
- `README.md` – Project documentation.
- `.gitignore` – Specifies files excluded from version control.

The database file is generated locally and is not included in the Git repository. This means each new installation starts with an empty database.

## 5. Getting Started

### Requirements
- Python 3 installed.
- Git installed.
- Visual Studio Code or another code editor.

### Installation

1. Clone the repository or download the project files.
2. Open a terminal in the project directory.
3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python -m streamlit run app.py
```

7. Open the local URL provided in the terminal, usually:

`http://localhost:8501`

### Database and Test Data

The SQLite database and its tables are created automatically when the application first runs. No separate database setup is required.

The application does not include preloaded sample data. Users can create fictional customer and staff records through the interface to test the main functionality.

## 6. Database Structure

The application uses SQLite to store information locally.

The database separates customer and staff information from job records.

The main data entities are:

- Customers
- Staff
- Jobs and appointments

Customer and staff records are linked to job records through their database IDs, allowing appointments to be assigned to the correct customer and staff member.

## 7. Architecture and Design Decisions

Python was selected because it is accessible, flexible and suitable for developing a small business application.

Streamlit was chosen because it allows a functional web interface to be developed quickly without requiring a separate frontend framework.

SQLite was selected because it provides a lightweight relational database without requiring a separate database server.

Appointments and jobs were combined into one workflow. This simplifies the system because an appointment can be treated as a scheduled job assigned to a member of staff.

The application uses separate files for the interface and database operations to make the code easier to understand and maintain.

Alternative approaches were considered. Flask or Django could have been used to develop the web application, but Streamlit was selected because it allowed the main functionality to be developed more quickly with a simpler structure. A database server such as PostgreSQL could also have been used, but SQLite was more appropriate for this small, local prototype.

## 8. Development Process

Development was completed in stages:

1. Set up the Python environment and installed dependencies.
2. Created the database structure and database functions.
3. Developed the customer management functionality.
4. Implemented customer onboarding statuses.
5. Developed staff management.
6. Implemented appointment booking and job management.
7. Added job status updates and staff deletion.
8. Tested the application using fictional customer and staff records.

## 9. Testing

Manual testing was carried out using fictional records.

The following functionality was tested:

- Creating and viewing customer records.
- Editing customer information.
- Updating onboarding statuses.
- Adding and viewing staff members.
- Deleting duplicate staff records.
- Booking appointments.
- Assigning staff to jobs.
- Updating job statuses.

Testing confirmed that the main workflows operated successfully.

## 10. Limitations and Future Improvements

The application is a basic prototype and is not intended for production use.

Potential improvements include:

- User authentication and role-based permissions.
- Improved input validation and error handling.
- More advanced appointment scheduling.
- Search and filtering functionality.
- A more detailed dashboard with operational statistics.
- Automated testing.
- Cloud hosting and database integration.

## 11. Use of AI Tools

AI development assistance was used to support code development, troubleshoot errors, explain technical concepts and assist with documentation.

Generated code was reviewed and tested within the application to verify that the implemented functionality worked as expected.

The development process also involved manually testing the main application workflows and resolving errors encountered during implementation.