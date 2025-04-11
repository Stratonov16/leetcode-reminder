import json
import random
from typing import Dict, Tuple

# Load messages from JSON
with open('reminders.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Import problems from your file
from striver_problems import problems

def get_random_problem() -> Tuple[str, str]:
    """Returns a random problem title and URL"""
    title = random.choice(list(problems.keys()))
    return title, problems[title]

def get_initial_message() -> str:
    return random.choice(messages['initial_messages'])

def get_reminder_message() -> str:
    return random.choice(messages['reminder_messages'])

def get_congrats_message() -> str:
    return random.choice(messages['congrats_messages'])

def get_problem_slug(url: str) -> str:
    """Extract problem slug from LeetCode URL"""
    return url.split('/')[-2]
