import hashlib
from repositories.user_repository import get_user_by_username, update_user_status


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password):
    user_row = get_user_by_username(username)

    if not user_row:
        return False, "User does not exist."

    user_id, db_username, db_password_hash, email, role, wrong_attempt, is_locked = user_row

    if is_locked == 1 or is_locked is True:
        return False, "This account is locked. Please contact support."

    hashed_input = hash_password(password)

    if hashed_input == db_password_hash:
        if wrong_attempt > 0:
            update_user_status(username, 0, False)
        return True, "Login successful!"
    else:
        new_attempts = wrong_attempt + 1
        lock_status = False

        if new_attempts >= 3:
            lock_status = True
            message = "Incorrect password. This account is now LOCKED!"
        else:
            message = f"Incorrect password. Attempt {new_attempts}/3."

        update_user_status(username, new_attempts, lock_status)
        return False, message
