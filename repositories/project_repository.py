from database.db_connection import get_connection
from models.project import Project


def create_project_from_hire(project_obj: Project, total_budget):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query_proj = """
                     INSERT INTO projects (job_id, client_id, freelancer_id, status)
                     VALUES (%s, %s, %s, %s) \
                     """
        cursor.execute(query_proj,
                       (project_obj.job_id, project_obj.client_id, project_obj.freelancer_id, project_obj.status))
        project_id = cursor.lastrowid

        query_m1 = "INSERT INTO project_milestones (project_id, title, amount, status) VALUES (%s, %s, %s, 'Active')"
        cursor.execute(query_m1, (project_id, 'Initial Deposit / Kickoff', total_budget * 0.30))

        query_m2 = "INSERT INTO project_milestones (project_id, title, amount, status) VALUES (%s, %s, %s, 'Active')"
        cursor.execute(query_m2, (project_id, 'Final Delivery & Review', total_budget * 0.70))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def get_projects_by_user(user_id, role):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        column = "client_id" if role == "Client" else "freelancer_id"
        query = f"""
            SELECT p.*, j.title AS job_title, u.username AS partner_username
            FROM projects p
            JOIN jobs j ON p.job_id = j.job_id
            JOIN users u ON u.user_id = (CASE WHEN %s = 'Client' THEN p.freelancer_id ELSE p.client_id END)
            WHERE p.{column} = %s
            ORDER BY p.created_at DESC
        """
        cursor.execute(query, (role, user_id))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()


def get_project_milestones(project_id):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM project_milestones WHERE project_id = %s"
        cursor.execute(query, (project_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()


def update_project_status(project_id, new_status):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE projects SET status = %s WHERE project_id = %s"
        cursor.execute(query, (new_status, project_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def update_milestone_status_with_payment(milestone_id, new_status, project_id):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor(dictionary=True)
    try:
        if new_status == "Finished":
            query_m_info = "SELECT title, amount FROM project_milestones WHERE milestone_id = %s"
            cursor.execute(query_m_info, (milestone_id,))
            m_data = cursor.fetchone()

            if not m_data:
                return False

            m_title = m_data['title']
            m_amount = m_data['amount']

            query_p_info = "SELECT client_id, freelancer_id FROM projects WHERE project_id = %s"
            cursor.execute(query_p_info, (project_id,))
            p_data = cursor.fetchone()

            if not p_data:
                return False

            client_id = p_data['client_id']
            freelancer_id = p_data['freelancer_id']

            query_deduct = "UPDATE clients SET budget = budget - %s WHERE user_id = %s"
            cursor.execute(query_deduct, (m_amount, client_id))

            query_earn = "INSERT INTO freelancer_history (user_id, job_title, earnings) VALUES (%s, %s, %s)"
            cursor.execute(query_earn, (freelancer_id, m_title, m_amount))

            query_update_m = """
                             UPDATE project_milestones
                             SET status       = 'Finished', \
                                 completed_at = CURRENT_TIMESTAMP
                             WHERE milestone_id = %s \
                             """
            cursor.execute(query_update_m, (milestone_id,))
        else:
            query_update_m = "UPDATE project_milestones SET status = %s WHERE milestone_id = %s"
            cursor.execute(query_update_m, (new_status, milestone_id))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in transaction: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def cancel_project_by_job_id(job_id):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE projects SET status = 'Canceled' WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def submit_review_and_update_rating(project_id, client_id, freelancer_id, rating, comment):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query_review = """
                       INSERT INTO reviews (project_id, client_id, freelancer_id, rating, comment)
                       VALUES (%s, %s, %s, %s, %s) \
                       """
        cursor.execute(query_review, (project_id, client_id, freelancer_id, rating, comment))

        query_avg = "SELECT AVG(rating) FROM reviews WHERE freelancer_id = %s"
        cursor.execute(query_avg, (freelancer_id,))
        new_avg = cursor.fetchone()[0]

        query_update_free = "UPDATE freelancers SET rating = %s WHERE user_id = %s"
        cursor.execute(query_update_free, (new_avg, freelancer_id))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error submitting review: {e}")
        return False
    finally:
        cursor.close()
        db.close()
