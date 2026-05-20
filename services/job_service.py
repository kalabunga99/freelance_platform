from models.job import Job
import repositories.job_repository as job_repository
import repositories.project_repository as project_repository

from repositories.job_repository import (
    add_job,
    get_jobs_by_client,
    update_job_status,
    update_job_deadline,
    get_all_open_jobs
)

def post_new_job(client_id, title, description, budget, deadline, seniority):
    new_job = Job(
        job_id=None,
        client_id=client_id,
        title=title,
        description=description,
        budget=budget,
        deadline=deadline,
        seniority=seniority,
        status="Open"
    )
    return add_job(new_job)

def get_client_jobs(client_id):
    return get_jobs_by_client(client_id)

def pause_job(job_id):
    return update_job_status(job_id, "Paused")

def close_job(job_id):
    return update_job_status(job_id, "Closed")

def extend_job_deadline(job_id, new_deadline):
    return update_job_deadline(job_id, new_deadline)

def get_available_jobs():
    return get_all_open_jobs()
def close_job(job_id):

    if job_repository.update_job_status(job_id, 'Closed'):
        project_repository.cancel_project_by_job_id(job_id)
        return True
    return False