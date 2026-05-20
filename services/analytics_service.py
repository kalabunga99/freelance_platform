import repositories.analytics_repository as analytics_repository


def get_client_dashboard_stats(client_id):
    data = analytics_repository.get_client_personal_stats(client_id)
    if not data:
        return {'total_posts': 0, 'hire_success_rate': 0.0, 'total_spent': 0.00}
    return data


def get_freelancer_dashboard_stats(freelancer_id):
    data = analytics_repository.get_freelancer_personal_stats(freelancer_id)
    if not data:
        return {'active_projects': 0, 'total_earnings': 0.00}
    return data


def get_platform_statistics_service():
    data = analytics_repository.get_global_platform_stats()
    if not data:
        return {
            'total_jobs': 0, 'hire_success_rate': 0.0, 'avg_fill_time_days': 0.0,
            'top_skills': [], 'monthly_revenue': 0.00, 'top_freelancers': []
        }
    return data
