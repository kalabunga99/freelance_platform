from models.conversation_thread import ConversationThread
from models.message import Message
import repositories.message_repository as msg_repository


def send_message(sender_id, receiver_id, body, subject=None):
    if not body or not body.strip():
        return {"success": False, "message": "Message body cannot be empty."}

    thread_result = msg_repository.get_thread_id_between_users(sender_id, receiver_id)

    if thread_result:
        thread_id = thread_result[0] if isinstance(thread_result, tuple) else thread_result.get('thread_id')
    else:
        new_thread = ConversationThread(client_id=sender_id, freelancer_id=receiver_id, subject=subject)
        thread_id = msg_repository.create_thread(new_thread)
        if not thread_id:
            return {"success": False, "message": "Failed to initialize conversation thread."}

    msg_obj = Message(thread_id=thread_id, sender_id=sender_id, body=body.strip())

    if msg_repository.add_message(msg_obj):
        msg_repository.update_last_read(thread_id, sender_id)
        return {"success": True, "message": "Message sent successfully.", "thread_id": thread_id}

    return {"success": False, "message": "Failed to deliver the message."}


def get_user_inbox(user_id, show_archived=0):
    return msg_repository.get_inbox_by_user(user_id, show_archived)


def open_conversation_thread(thread_id, user_id):
    msg_repository.update_last_read(thread_id, user_id)
    return msg_repository.get_messages_by_thread(thread_id)


def toggle_archive_thread(thread_id, user_id, archive_status):
    status_val = 1 if archive_status else 0
    if msg_repository.update_archive_status(thread_id, user_id, status_val):
        return {"success": True, "message": "Thread archive status updated."}
    return {"success": False, "message": "Failed to update archive status."}


def search_inbox_messages(user_id, keyword):
    if not keyword or not keyword.strip():
        return []
    return msg_repository.search_messages_by_user(user_id, keyword.strip())
