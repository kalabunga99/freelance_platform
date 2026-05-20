from database.db_connection import get_connection


def get_client_personal_stats(client_id):
    db = get_connection()
    if not db:
        return None

    cursor = db.cursor(dictionary=True)
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) AS total_posts FROM jobs WHERE client_id = %s", (client_id,))
        stats['total_posts'] = cursor.fetchone()['total_posts']

        query_success = """
            SELECT 
                (SELECT COUNT(*) FROM jobs WHERE client_id = %s AND status IN ('In Progress', 'Closed')) AS filled,
                COUNT(*) AS total 
            FROM jobs WHERE client_id = %s
        """
        cursor.execute(query_success, (client_id, client_id))
        res = cursor.fetchone()
        stats['hire_success_rate'] = round((res['filled'] / res['total']) * 100, 1) if res['total'] > 0 else 0.0

        query_spent = """
            SELECT SUM(pm.amount) AS total_spent 
            FROM project_milestones pm
            JOIN projects p ON pm.project_id = p.project_id
            WHERE p.client_id = %s AND pm.status = 'Finished'
        """
        cursor.execute(query_spent, (client_id,))
        spent_data = cursor.fetchone()
        stats['total_spent'] = float(spent_data['total_spent']) if spent_data['total_spent'] else 0.00

        return stats
    except Exception as e:
        print(f"Error fetching client stats: {e}")
        return None
    finally:
        cursor.close()
        db.close()


def get_freelancer_personal_stats(freelancer_id):
    db = get_connection()
    if not db:
        return None

    cursor = db.cursor(dictionary=True)
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) AS active_projects FROM projects WHERE freelancer_id = %s AND status = 'Active'", (freelancer_id,))
        stats['active_projects'] = cursor.fetchone()['active_projects']

        cursor.execute("SELECT SUM(earnings) AS total_earnings FROM freelancer_history WHERE user_id = %s", (freelancer_id,))
        earn_data = cursor.fetchone()
        stats['total_earnings'] = float(earn_data['total_earnings']) if earn_data['total_earnings'] else 0.00

        return stats
    except Exception as e:
        print(f"Error fetching freelancer stats: {e}")
        return None
    finally:
        cursor.close()
        db.close()


def get_global_platform_stats():
    db = get_connection()
    if not db:
        return None

    cursor = db.cursor(dictionary=True)
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) AS total_jobs FROM jobs")
        stats['total_jobs'] = cursor.fetchone()['total_jobs']

        query_rate = """
            SELECT 
                (SELECT COUNT(*) FROM jobs WHERE status IN ('In Progress', 'Closed')) AS filled,
                COUNT(*) AS total 
            FROM jobs
        """
        cursor.execute(query_rate)
        rate_data = cursor.fetchone()
        stats['hire_success_rate'] = round((rate_data['filled'] / rate_data['total']) * 100, 1) if rate_data['total'] > 0 else 0.0

        query_time = """
            SELECT AVG(TIMESTAMPDIFF(DAY, j.deadline, p.created_at)) AS avg_days
            FROM jobs j
            JOIN projects p ON j.job_id = p.job_id
        """
        cursor.execute(query_time)
        time_data = cursor.fetchone()
        stats['avg_fill_time_days'] = round(abs(time_data['avg_days']), 1) if time_data['avg_days'] else 0.0

        query_skills = """
            SELECT skill_name, COUNT(*) AS skill_count 
            FROM freelancer_skills 
            GROUP BY skill_name 
            ORDER BY skill_count DESC 
            LIMIT 3
        """
        cursor.execute(query_skills)
        stats['top_skills'] = cursor.fetchall()

        query_rev = "SELECT SUM(earnings) AS monthly_revenue FROM freelancer_history"
        cursor.execute(query_rev)
        rev_data = cursor.fetchone()
        stats['monthly_revenue'] = float(rev_data['monthly_revenue']) if rev_data['monthly_revenue'] else 0.00

        query_top = "SELECT name, rating FROM freelancers ORDER BY rating DESC LIMIT 3"
        cursor.execute(query_top)
        stats['top_freelancers'] = cursor.fetchall()

        return stats
    except Exception as e:
        print(f"Error fetching global analytics: {e}")
        return None
    finally:
        cursor.close()
        db.close()
