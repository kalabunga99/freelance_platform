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