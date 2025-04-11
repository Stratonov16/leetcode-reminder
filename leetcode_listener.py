import requests
import time
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def check_submission(username: str, problem_slug: str) -> bool:
    """
    Check if user has submitted a solution for the problem
    Returns True if problem is solved, False otherwise
    """
    try:
        # LeetCode GraphQL API endpoint
        url = "https://leetcode.com/graphql"

        # GraphQL query to get recent submissions
        query = """
        query recentSubmissions($username: String!) {
          recentSubmissionList(username: $username) {
            title
            statusDisplay
            timestamp
          }
        }
        """

        # Send request to LeetCode API
        response = requests.post(url, json={
            'query': query,
            'variables': {'username': username}
        })

        if response.status_code == 200:
            data = response.json()
            submissions = data.get('data', {}).get('recentSubmissionList', [])

            # Check last 24 hours submissions
            current_time = datetime.now().timestamp()
            day_ago = current_time - (24 * 60 * 60)

            for submission in submissions:
                # Convert timestamp to float if it's a string
                submission_time = float(submission['timestamp'])
                if (submission['title'].lower().replace(' ', '-') == problem_slug and
                    submission['statusDisplay'] == 'Accepted' and
                    submission_time > day_ago):
                    return True

        return False

    except Exception as e:
        logging.error(f"Error checking submission: {str(e)}")
        return False

def listen_for_submission(username: str, problem_slug: str) -> bool:
    """
    Check for submission once and return result
    """
    try:
        return check_submission(username, problem_slug)
    except Exception as e:
        logging.error(f"Error in submission listener: {str(e)}")
        return False
