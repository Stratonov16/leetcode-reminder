import logging

import requests


class SlackSender:
    def __init__(self, problem_webhook_url: str, congrats_webhook_url: str):
        self.problem_webhook_url = problem_webhook_url
        self.congrats_webhook_url = congrats_webhook_url
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='slack_sender.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def send_problem_message(self, title: str, msg: str, url: str) -> bool:
        """
        Send message to Slack using the problem workflow
        (uses all three parameters: title, msg, url)
        """
        try:
            payload = {
                "title": title,
                "msg": msg,
                "url": url
            }
            logging.info(f"Sending problem: {title}")
            response = requests.post(self.problem_webhook_url, json=payload)
            
            if response.status_code != 200:
                logging.error(f"Failed to send problem message: {response.text}")
                return False
                
            logging.info(f"Successfully sent problem message for: {title}")
            return True
            
        except Exception as e:
            logging.error(f"Error sending problem message: {str(e)}")
            return False

    def send_congrats_message(self, msg: str) -> bool:
        """
        Send message to Slack using the congratulations workflow
        (uses only msg parameter)
        """
        try:
            payload = {
                "msg": msg
            }
            
            response = requests.post(self.congrats_webhook_url, json=payload)
            
            if response.status_code != 200:
                logging.error(f"Failed to send congrats message: {response.text}")
                return False
                
            logging.info(f"Successfully sent congrats message")
            return True
            
        except Exception as e:
            logging.error(f"Error sending congrats message: {str(e)}")
            return False

# Initialize the sender with your webhook URLs
slack_sender = SlackSender(
    ##TODO: Add your slack channel webhook url here
    problem_webhook_url ="https://hooks.slack.com/triggers/",
    congrats_webhook_url = "https://hooks.slack.com/triggers/"
)

# Functions to be used by other modules
def send_slack_message(title: str, msg: str, url: str, is_congrats: bool = False) -> bool:
    if is_congrats:
        # For congrats messages, we'll combine title into the message
        combined_msg = f"{msg} {title}"
        return slack_sender.send_congrats_message(combined_msg)
    else:
        return slack_sender.send_problem_message(title, msg, url)
