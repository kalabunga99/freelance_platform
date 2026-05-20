from repositories.user_repository import (
    get_client_profile,
    update_client_profile,
    get_freelancer_profile,
    update_freelancer_profile,
    add_freelancer_skill,
    get_freelancer_skills,
    get_freelancer_languages,
    add_freelancer_language,
    get_freelancer_portfolio,
    add_freelancer_portfolio,
    get_freelancer_history
)
import repositories.user_repository as user_repository


def get_profile_data(user_id):
    return get_client_profile(user_id)


def save_profile_data(user_id, company_name):
    return update_client_profile(user_id, company_name)


def deposit_funds_service(user_id, amount):
    if amount <= 0:
        return False
    return user_repository.update_client_balance(user_id, amount)


def get_free_profile_data(user_id):
    return get_freelancer_profile(user_id)


def save_free_profile_data(user_id, name, years_of_experience):
    return update_freelancer_profile(user_id, name, years_of_experience)


def get_skills(user_id):
    return get_freelancer_skills(user_id)


def save_new_skill(user_id, skill_name):
    if not skill_name or not skill_name.strip():
        return False
    return add_freelancer_skill(user_id, skill_name.strip())


def get_languages(user_id):
    return get_freelancer_languages(user_id)


def save_new_language(user_id, language_name):
    if not language_name or not language_name.strip():
        return False
    return add_freelancer_language(user_id, language_name.strip())


def get_portfolio(user_id):
    return get_freelancer_portfolio(user_id)


def save_new_portfolio(user_id, link_url):
    if not link_url or not link_url.strip():
        return False
    return add_freelancer_portfolio(user_id, link_url.strip())


def get_history(user_id):
    return get_freelancer_history(user_id)
