from models.application import Application
import repositories.app_repository as app_repository


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

