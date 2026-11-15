import sqlite3

DB_NAME = "smarti.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialise_database():
    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT NOT NULL,
                onboarding_status TEXT DEFAULT 'New Enquiry'
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                staff_id INTEGER,
                description TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (staff_id) REFERENCES staff(id)
            )
        """)


def add_customer(name, email, phone, address):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO customers (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, address))


def get_customers():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM customers ORDER BY name"
        ).fetchall()


def update_customer(customer_id, name, email, phone, address, status):
    with get_connection() as conn:
        conn.execute("""
            UPDATE customers
            SET name=?, email=?, phone=?, address=?,
                onboarding_status=?
            WHERE id=?
        """, (name, email, phone, address, status, customer_id))


def update_customer_status(customer_id, status):
    with get_connection() as conn:
        conn.execute("""
            UPDATE customers
            SET onboarding_status=?
            WHERE id=?
        """, (status, customer_id))


def add_staff(name, role):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO staff (name, role)
            VALUES (?, ?)
        """, (name, role))


def get_staff():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM staff ORDER BY name"
        ).fetchall()
def delete_staff(staff_id):
    with get_connection() as conn:
        assigned = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE staff_id=?",
            (staff_id,)
        ).fetchone()[0]

        if assigned:
            raise ValueError("Cannot delete staff assigned to existing jobs.")

        conn.execute(
            "DELETE FROM staff WHERE id=?",
            (staff_id,)
        )

def add_job(customer_id, staff_id, description, date, time):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO jobs
            (customer_id, staff_id, description,
             appointment_date, appointment_time)
            VALUES (?, ?, ?, ?, ?)
        """, (customer_id, staff_id, description, date, time))


def get_jobs():
    with get_connection() as conn:
        return conn.execute("""
            SELECT jobs.id, customers.name, jobs.description,
                   jobs.appointment_date, jobs.appointment_time,
                   staff.name, jobs.status
            FROM jobs
            JOIN customers ON jobs.customer_id = customers.id
            LEFT JOIN staff ON jobs.staff_id = staff.id
            ORDER BY jobs.appointment_date, jobs.appointment_time
        """).fetchall()


def update_job_status(job_id, status):
    with get_connection() as conn:
        conn.execute("""
            UPDATE jobs SET status=?
            WHERE id=?
        """, (status, job_id))


def get_dashboard_counts():
    with get_connection() as conn:
        customers = conn.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        active = conn.execute(
            "SELECT COUNT(*) FROM customers WHERE onboarding_status='Active'"
        ).fetchone()[0]

        pending = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE status='Pending'"
        ).fetchone()[0]

        completed = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE status='Completed'"
        ).fetchone()[0]

        return customers, active, pending, completed