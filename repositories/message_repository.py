from database.db_connection import get_connection
from models.conversation_thread import ConversationThread
from models.message import Message


def create_thread(thread_obj: ConversationThread):
    db = get_connection()
    if not db:
        return None

    cursor = db.cursor()
    try:
        query = """
                INSERT INTO conversation_threads (client_id, freelancer_id, subject)
                VALUES (%s, %s, %s)
                """
        cursor.execute(query, (thread_obj.client_id, thread_obj.freelancer_id, thread_obj.subject))
        db.commit()
        thread_id = cursor.lastrowid

        query_part = "INSERT INTO thread_participants (thread_id, user_id) VALUES (%s, %s), (%s, %s)"
        cursor.execute(query_part, (thread_id, thread_obj.client_id, thread_id, thread_obj.freelancer_id))
        db.commit()

        return thread_id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()


def get_thread_id_between_users(user1_id, user2_id):
    db = get_connection()
    if not db:
        return None

    cursor = db.cursor()
    try:
        query = """
                SELECT thread_id \
                FROM conversation_threads
                WHERE (client_id = %s AND freelancer_id = %s)
                   OR (client_id = %s AND freelancer_id = %s)
                """
        cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()


def add_message(msg_obj: Message):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "INSERT INTO messages (thread_id, sender_id, body) VALUES (%s, %s, %s)"
        cursor.execute(query, (msg_obj.thread_id, msg_obj.sender_id, msg_obj.body))

        query_update_thread = "UPDATE conversation_threads SET updated_at = CURRENT_TIMESTAMP WHERE thread_id = %s"
        cursor.execute(query_update_thread, (msg_obj.thread_id,))

        query_reset_archive = "UPDATE thread_participants SET is_archived = 0 WHERE thread_id = %s"
        cursor.execute(query_reset_archive, (msg_obj.thread_id,))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def get_inbox_by_user(user_id, show_archived=0):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = """
                SELECT t.thread_id, \
                       t.subject, \
                       t.updated_at, \
                       u.username AS                                                                     participant_username, \
                       u.user_id  AS                                                                     participant_id, \
                       (SELECT body FROM messages WHERE thread_id = t.thread_id ORDER BY created_at DESC LIMIT 1) AS last_message,
                    (SELECT COUNT(*) FROM messages m 
                     WHERE m.thread_id = t.thread_id 
                       AND m.sender_id != %s
                    AND m.created_at > p.last_read_at) AS unread_count
                FROM conversation_threads t
                    JOIN thread_participants p \
                ON t.thread_id = p.thread_id
                    JOIN thread_participants op ON t.thread_id = op.thread_id AND op.user_id != %s
                    JOIN users u ON op.user_id = u.user_id
                WHERE p.user_id = %s \
                  AND p.is_archived = %s
                ORDER BY t.updated_at DESC
                """
        cursor.execute(query, (user_id, user_id, user_id, show_archived))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()


def get_messages_by_thread(thread_id):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = """
                SELECT m.*, u.username AS sender_username
                FROM messages m
                         JOIN users u ON m.sender_id = u.user_id
                WHERE m.thread_id = %s
                ORDER BY m.created_at ASC
                """
        cursor.execute(query, (thread_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()


def update_last_read(thread_id, user_id):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE thread_participants SET last_read_at = CURRENT_TIMESTAMP WHERE thread_id = %s AND user_id = %s"
        cursor.execute(query, (thread_id, user_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def update_archive_status(thread_id, user_id, is_archived):
    db = get_connection()
    if not db:
        return False

    cursor = db.cursor()
    try:
        query = "UPDATE thread_participants SET is_archived = %s WHERE thread_id = %s AND user_id = %s"
        cursor.execute(query, (is_archived, thread_id, user_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()


def search_messages_by_user(user_id, keyword):
    db = get_connection()
    if not db:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        query = """
                SELECT m.message_id, m.thread_id, m.body, m.created_at, t.subject, u.username AS sender_username
                FROM messages m
                         JOIN conversation_threads t ON m.thread_id = t.thread_id
                         JOIN thread_participants p ON t.thread_id = p.thread_id
                         JOIN users u ON m.sender_id = u.user_id
                WHERE p.user_id = %s \
                  AND m.body LIKE %s
                ORDER BY m.created_at DESC
                """
        cursor.execute(query, (user_id, f"%{keyword}%"))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        db.close()
