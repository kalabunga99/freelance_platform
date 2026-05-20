from database.db_connection import get_connection
from models.application import Application

def add_application(app_obj: Application):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = """
                INSERT INTO applications (job_id, freelancer_id, cover_letter, proposed_price, proposed_deadline)
                VALUES (%s, %s, %s, %s, %s)
                """
        data = (
            app_obj.job_id,
            app_obj.freelancer_id,
            app_obj.cover_letter,
            app_obj.proposed_price,
            app_obj.proposed_deadline
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


def get_applications_by_job(job_id, sort_by=None):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = """
                SELECT a.application_id, \
                       a.job_id, \
                       a.freelancer_id, \
                       a.cover_letter, \
                       a.proposed_price, \
                       a.proposed_deadline, \
                       a.created_at, \
                       f.name   AS freelancer_name, \
                       f.years_of_experience, \
                       f.rating AS freelancer_rating
                FROM applications a
                         JOIN freelancers f ON a.freelancer_id = f.user_id
                WHERE a.job_id = %s
                """

        if sort_by == "cena":
            query += " ORDER BY a.proposed_price ASC"
        elif sort_by == "iskustvo":
            query += " ORDER BY f.years_of_experience DESC"
        elif sort_by == "ocena":
            query += " ORDER BY f.rating DESC"

        cursor.execute(query, (job_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()
def get_applications_by_freelancer(freelancer_id):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = """
                SELECT 
                    a.application_id,
                    a.job_id,
                    a.cover_letter,
                    a.proposed_price,
                    a.proposed_deadline,
                    a.created_at,
                    j.title AS job_title,
                    j.status AS job_status
                FROM applications a
                JOIN jobs j ON a.job_id = j.job_id
                WHERE a.freelancer_id = %s
                ORDER BY a.created_at DESC
                """
        cursor.execute(query, (freelancer_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()

