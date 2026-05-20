from models.project import Project
import repositories.project_repository as project_repository


def start_new_project(job_id, client_id, freelancer_id, total_budget):
    proj_obj = Project(job_id=job_id, client_id=client_id, freelancer_id=freelancer_id, status='Active')
    return project_repository.create_project_from_hire(proj_obj, total_budget)


def get_user_projects(user_id, role):
    return project_repository.get_projects_by_user(user_id, role)


def get_milestones(project_id):
    return project_repository.get_project_milestones(project_id)


def change_project_status(project_id, status):
    valid_statuses = ['Active', 'Review', 'Finished', 'Canceled']
    if status in valid_statuses:
        return project_repository.update_project_status(project_id, status)
    return False


def change_milestone_status(milestone_id, status, project_id):
    valid_statuses = ['Active', 'Review', 'Finished', 'Canceled']
    if status in valid_statuses:
        return project_repository.update_milestone_status_with_payment(milestone_id, status, project_id)
    return False
def leave_freelancer_review(project_id, client_id, freelancer_id, rating, comment):
    if rating < 1 or rating > 5:
        return False
    return project_repository.submit_review_and_update_rating(project_id, client_id, freelancer_id, rating, comment.strip())

