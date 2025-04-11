
```markdown
# LeetCode Practice Reminder Bot

A Python-based Slack bot that helps maintain consistent LeetCode practice by sending scheduled reminders on slack and tracking problem completion. 

## Overview

This bot automatically:
- Selects a random LeetCode problem daily out of list. 
- Sends reminders at scheduled times
- Monitors problem completion status
- Sends congratulatory messages upon successful submission
- Increases reminder frequency in the evening if problem remains unsolved

## Project Structure

```
leetcode_reminder/
├── main.py                 # Main script handling scheduling and coordination
├── leetcode_listener.py    # LeetCode API integration for submission checking
├── slack_sender.py        # Slack message sending functionality
├── messages.py            # Message templates and problem selection
├── reminders.json         # Message templates for different scenarios
├── requirements.txt       # Python dependencies
```

## Prerequisites

- Python 3.8+
- Slack Workspace with permission to create workflows
- LeetCode account

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd leetcode_reminder
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set up Slack workflows:
    - Create two workflows in your Slack workspace:
        1. Problem workflow (accepts title, msg, link)
        2. Congratulations workflow (accepts msg)
    - Get webhook URLs for both workflows

2. Configure the script:
    - Update LEETCODE_USERNAME in main.py
    - Update webhook URLs in slack_sender.py

## Schedule

The bot follows this reminder schedule:
- 12:00 AM: New problem assignment
- 9:00 AM: First reminder
- 4:00 PM: Second reminder
- 7:00 PM: Third reminder
- 9:00 PM: Fourth reminder
- After 9:00 PM: Reminders every 29 minutes until midnight

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Start monitoring immediately
2. Send an initial problem
3. Follow the reminder schedule
4. Check for problem completion every minute
5. Send congratulations when the problem is solved

## Logging

The script creates a log file (`leetcode_reminder.log` and `slack_sender.log`)

## Files Description

- `main.py`: Main script coordinating all components
- `leetcode_listener.py`: Handles LeetCode API integration
- `slack_sender.py`: Manages Slack message sending
- `messages.py`: Contains message templates and problem selection logic
- `reminders.json`: Stores various message templates
- `transform.py`: Takes striver sde sheet response and filter only leetcode problems and insert it in striver_problems.py

## Error Handling

The script includes comprehensive error handling for:
- API failures
- Network issues
- Invalid responses
- Schedule conflicts

## Dependencies

- requests==2.31.0
- schedule==1.2.0
- python-dotenv==1.0.0 (optional)

