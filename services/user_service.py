from repositories.user_repository import (
    get_client_profile,
    update_client_profile,
    get_freelancer_profile,
    update_freelancer_profile
)

def get_profile_data(user_id):
    return get_client_profile(user_id)

def save_profile_data(user_id, company_name, budget):
    return update_client_profile(user_id, company_name, budget)

def get_free_profile_data(user_id):
    return get_freelancer_profile(user_id)

def save_free_profile_data(user_id, name, years_of_experience):
    return update_freelancer_profile(user_id, name, years_of_experience)
