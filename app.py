import os
import time
import environ

from jinja2 import Environment, FileSystemLoader

from utils import (
    check_availability, send_mail, format_json_data, get_date
)

# reading .env file
env = environ.Env()
environ.Env.read_env()

BASE_DIR = os.path.join(os.path.dirname(__file__), '.')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates/')

FROM_EMAIL = env('FROM_EMAIL', default=None)
TO_EMAIL = env('TO_EMAIL', default=None)

# Default 60*60 = 3600 (1hour)
TIME_IN_SECONDS = env('TIME_IN_SECONDS', default=3600)

DISTRICT_ID = env('DISTRICT_ID', default=None)
PINCODE = env('PINCODE', default=None)
AGE = env('AGE', default=45)
DATE = env('DATE', default=get_date())


def cowin_notify():
    try:
        # Fetch data from API
        json_data = format_json_data(
            check_availability(
                district_id=DISTRICT_ID, pincode=PINCODE, age=AGE, date=DATE
            )
        )

        if json_data:
            # Create HTML body content
            template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
            template = template_env.get_template('email.html')
            msg_body = template.render(data=json_data)

            # Send Mail
            from_email = FROM_EMAIL
            to_email = TO_EMAIL
            subject = 'CoWin Slot Availability - Notification'
            send_mail(from_email, to_email, subject, msg_body)
            print('Slot Available and Email Send Successfully')
        else:
            print('No Slot Available')
    except Exception as e:
        print('Exception: ', str(e))


if __name__ == "__main__":
    while True:
        time.sleep(TIME_IN_SECONDS)
        cowin_notify()
