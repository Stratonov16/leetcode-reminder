import logging
import schedule
import time
from datetime import datetime, timedelta

from messages import get_random_problem, get_initial_message, get_reminder_message, get_congrats_message, get_problem_slug
from slack_sender import send_slack_message
from leetcode_listener import listen_for_submission

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[
                       logging.StreamHandler(),
                       logging.FileHandler('leetcode_reminder.log')
                   ])

LEETCODE_USERNAME = "stratonov16" #### TODO: add your user name here

class LeetCodeScheduler:
    def __init__(self):
        self.current_problem = None
        self.problem_solved = False
        self.last_check_time = None
        logging.debug("Initializing LeetCodeScheduler")

    def new_problem_cycle(self):
        """Start a new problem cycle"""
        logging.info("Starting new problem cycle")
        self.current_problem = get_random_problem()
        self.problem_solved = False
        title, link = self.current_problem
        self._send_initial_message(title, link)
        logging.debug(f"New problem selected: {title}")

    def _send_initial_message(self, title, link):
        """Send initial message for new problem"""
        try:
            msg = get_initial_message()
            send_slack_message(title, msg, link, False)
        except Exception as e:
            logging.error(f"Error sending initial message: {str(e)}")

    def check_problem_completion(self):
        """Check if problem is solved (runs every minute)"""
        if not self.problem_solved and self.current_problem:
            try:
                title, link = self.current_problem
                problem_slug = get_problem_slug(link)
                if listen_for_submission(LEETCODE_USERNAME, problem_slug):
                    self.problem_solved = True
                    self._send_congrats_message(title, link)
                    logging.info(f"Problem solved: {title}")
                    return True
            except Exception as e:
                logging.error(f"Error checking problem completion: {str(e)}")
        return False

    def _send_congrats_message(self, title, link):
        """Send congratulation message"""
        try:
            msg = get_congrats_message()
            send_slack_message(title, msg, link, True)
        except Exception as e:
            logging.error(f"Error sending congrats message: {str(e)}")

    def check_and_send_reminder(self):
        """Send reminder if not solved (at scheduled times)"""
        if not self.problem_solved and self.current_problem:
            try:
                logging.debug("Sending scheduled reminder")
                title, link = self.current_problem
                msg = get_reminder_message()
                send_slack_message(title, msg, link, False)
                logging.debug("Reminder sent")
            except Exception as e:
                logging.error(f"Error sending reminder: {str(e)}")

    def schedule_rapid_reminders(self):
        """Schedule rapid reminders after 9 PM"""
        if self.problem_solved:
            logging.debug("Problem already solved, no need for rapid reminders")
            return

        try:
            current_time = datetime.now()
            next_time = get_next_reminder_time(current_time)

            if next_time:
                logging.debug(f"Scheduling next rapid reminder for {next_time}")
                schedule.every().day.at(next_time.strftime("%H:%M")).do(
                    self.check_and_send_reminder
                )
        except Exception as e:
            logging.error(f"Error scheduling rapid reminders: {str(e)}")

def get_next_reminder_time(current_time):
    """Calculate next reminder time after 9 PM with reducing intervals"""
    if current_time.hour < 21:  # Before 9 PM
        return current_time.replace(hour=21, minute=0, second=0)

    # After 9 PM, reduce interval by 29 minutes each time
    next_time = current_time + timedelta(minutes=29)
    if next_time.hour >= 0 and next_time.hour < 12:  # If we cross midnight
        return None
    return next_time

def main():
    logging.info("Starting LeetCode Reminder script")
    scheduler = LeetCodeScheduler()

    # Schedule fixed time reminders
    schedule.every().day.at("00:00").do(scheduler.new_problem_cycle)
    schedule.every().day.at("09:00").do(scheduler.check_and_send_reminder)
    schedule.every().day.at("16:00").do(scheduler.check_and_send_reminder)
    schedule.every().day.at("19:00").do(scheduler.check_and_send_reminder)
    schedule.every().day.at("21:00").do(scheduler.check_and_send_reminder)

    # Schedule rapid reminders after 9 PM
    schedule.every().day.at("21:00").do(scheduler.schedule_rapid_reminders)

    logging.debug("All schedules set")

    # Start with a new problem immediately
    scheduler.new_problem_cycle()
    logging.debug("Initial problem cycle started")

    try:
        while True:
            schedule.run_pending()
            # Check for problem completion every minute
            if scheduler.check_problem_completion():
                logging.info("Problem completed! Waiting for next cycle.")
            time.sleep(60)  # Check every minute
            logging.debug("Scheduler loop running")
    except KeyboardInterrupt:
        logging.info("Script stopped by user")
    except Exception as e:
        logging.exception("Unexpected error occurred")

if __name__ == "__main__":
    try:
        logging.info("Program started")
        main()
    except Exception as e:
        logging.exception(f"Error occurred: {str(e)}")
