from database.db_connection import get_connection
from models.job import Job


def add_job(job_obj: Job):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = """
                INSERT INTO jobs (client_id, title, description, budget, deadline, seniority, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s) \
                """
        data = (
            job_obj.client_id,
            job_obj.title,
            job_obj.description,
            job_obj.budget,
            job_obj.deadline,
            job_obj.seniority,
            job_obj.status
        )
        cursor.execute(query, data)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def get_jobs_by_client(client_id):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor()
    try:
        query = "SELECT * FROM jobs WHERE client_id = %s"
        cursor.execute(query, (client_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()


def update_job_status(job_id, new_status):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE jobs SET status = %s WHERE job_id = %s"
        cursor.execute(query, (new_status, job_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def update_job_deadline(job_id, new_deadline):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE jobs SET deadline = %s WHERE job_id = %s"
        cursor.execute(query, (new_deadline, job_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def get_all_open_jobs():
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor()
    try:
        query = "SELECT * FROM jobs WHERE status = 'Open'"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()
