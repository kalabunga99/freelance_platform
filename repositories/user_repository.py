from database.db_connection import get_connection
from models.user import User
from models.client import Client
from models.freelancer import Freelancer


def add_user(user_obj: User | Client | Freelancer):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()

    try:
        query_user = "INSERT INTO users (username, password_hash, email, role) VALUES (%s, %s, %s, %s)"
        user_data = (user_obj.username, user_obj.password, user_obj.email, user_obj.role)
        cursor.execute(query_user, user_data)

        generated_id = cursor.lastrowid

        if user_obj.role == "Client":
            query_client = "INSERT INTO clients (user_id, company_name) VALUES (%s, %s)"
            client_data = (generated_id, user_obj.company_name)
            cursor.execute(query_client, client_data)

        elif user_obj.role == "Freelancer":
            query_freelance = "INSERT INTO freelancers (user_id, name) VALUES (%s, %s)"
            freelance_data = (generated_id, user_obj.name)
            cursor.execute(query_freelance, freelance_data)

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        db.close()

def get_user_by_username(username):
    db = get_connection()
    cursor = db.cursor()
    try:
        query_user = "SELECT * FROM users WHERE username = %s"
        user_data = (username,)
        cursor.execute(query_user, user_data)

        user_row = cursor.fetchone()
        return user_row

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()

def update_user_status(username, wrong_attempt, is_locked):
    db = get_connection()
    if not db:
        return False
    cursor = db.cursor()
    try:
        sql_locked = 1 if is_locked else 0
        query = "UPDATE users SET wrong_attempt = %s, is_locked = %s WHERE username = %s"
        cursor.execute(query, (wrong_attempt, sql_locked, username))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def get_client_profile(user_id):
    db = get_connection()
    if not db:
        return None
    cursor = db.cursor()
    try:
        query = """
            SELECT u.username, u.email, c.company_name, c.budget, c.average_grade 
            FROM users u 
            JOIN clients c ON u.user_id = c.user_id 
            WHERE u.user_id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()

def update_client_profile(user_id, company_name, budget):
    db = get_connection()
    if not db:
        return False
    cursor = db.cursor()
    try:
        query = "UPDATE clients SET company_name = %s, budget = %s WHERE user_id = %s"
        cursor.execute(query, (company_name, budget, user_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
def get_freelancer_profile(user_id):
    db = get_connection()
    if not db:
        return None
    cursor = db.cursor()
    try:
        query = """
            SELECT u.username, u.email, f.name, f.years_of_experience, f.rating 
            FROM users u 
            JOIN freelancers f ON u.user_id = f.user_id 
            WHERE u.user_id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()

def update_freelancer_profile(user_id, name, years_of_experience):
    db = get_connection()
    if not db:
        return False
    cursor = db.cursor()
    try:
        query = "UPDATE freelancers SET name = %s, years_of_experience = %s WHERE user_id = %s"
        cursor.execute(query, (name, years_of_experience, user_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
