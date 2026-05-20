from models.application import Application
import repositories.app_repository as app_repository
import repositories.user_repository as user_repository


def submit_application(job_id, freelancer_id, cover_letter, price, deadline):
    if price <= 0:
        return {"success": False, "message": "Cena mora biti veća od nule."}

    if not cover_letter or not cover_letter.strip():
        return {"success": False, "message": "Motivaciona poruka ne može biti prazna."}

    app_obj = Application(
        job_id=job_id,
        freelancer_id=freelancer_id,
        cover_letter=cover_letter.strip(),
        proposed_price=price,
        proposed_deadline=deadline
    )

    result = app_repository.add_application(app_obj)

    if result:
        return {"success": True, "message": "Uspešno ste aplicirali na posao!"}
    else:
        return {"success": False, "message": "Greška pri prijavi. Moguće je da ste već aplicirali na ovaj posao."}


def get_sorted_applications_for_client(job_id, criteria):
    valid_criteria = ["cena", "iskustvo", "ocena"]
    sort_by = criteria if criteria in valid_criteria else None

    return app_repository.get_applications_by_job(job_id, sort_by=sort_by)

def get_freelancer_proposals(freelancer_id):
    return app_repository.get_applications_by_freelancer(freelancer_id)
def hire_freelancer_service(job_id, client_id, freelancer_id, job_title, total_budget):
    client_profile = user_repository.get_profile_data(client_id)
    if client_profile:
        username, email, company_name, current_balance, average_grade = client_profile
        if current_balance < float(total_budget):
            return {"success": False, "message": f"Insufficient funds. Your balance is ${current_balance:.2f}, but the proposal requires ${float(total_budget):.2f}."}

    result = app_repository.hire_freelancer_transaction(job_id, client_id, freelancer_id, job_title, total_budget)
    if result:
        return {"success": True, "message": "Successfully hired the freelancer!"}
    return {"success": False, "message": "Database error occurred during hiring."}

