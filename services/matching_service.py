import repositories.app_repository as app_repository


def get_top_candidates_for_job(job_id):
    apps = app_repository.get_applications_by_job(job_id, sort_by=None)
    if not apps:
        return []

    job_budget = 400.00
    job_deadline = 15

    ranked_candidates = []

    for app in apps:
        app_price = float(app['proposed_price'])
        app_deadline = int(app['proposed_deadline'])
        rating = float(app['freelancer_rating'])
        experience = int(app['years_of_experience'])

        skill_score = 100.0

        if app_price > job_budget:
            price_score = 100.0 * (1.0 - (app_price - job_budget) / job_budget)
        else:
            price_score = 100.0
        price_score = max(0.0, min(100.0, price_score))

        if app_deadline > job_deadline:
            delivery_score = 100.0 * (1.0 - (app_deadline - job_deadline) / job_deadline)
        else:
            delivery_score = 100.0
        delivery_score = max(0.0, min(100.0, delivery_score))

        rating_score = (rating / 5.0) * 100.0
        experience_score = min(100.0, experience * 15.0)

        final_score = (skill_score * 0.30) + (rating_score * 0.20) + (price_score * 0.20) + (delivery_score * 0.15) + (
                    experience_score * 0.15)

        app['ai_score'] = round(final_score, 2)
        ranked_candidates.append(app)

    ranked_candidates.sort(key=lambda x: x['ai_score'], reverse=True)
    return ranked_candidates[:5]
