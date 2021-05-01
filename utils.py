import environ
import requests

from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# reading .env file
env = environ.Env()
environ.Env.read_env()

EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=None)


def get_date():
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d/%m/%Y')
    return tomorrow_formatted


def search_by_district(district_id, date):
    """
        Search Availability By District
    """
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/' \
          f'calendarByDistrict?district_id={district_id}&date={date}'

    try:
        request = requests.get(url, headers={})
        json_data = request.json()
        if request.status_code == 200:
            return json_data
        else:
            print('Error: ', str(json_data))
    except Exception as e:
        print('Exception: ', str(e))


def search_by_pin(pincode, date):
    """
        Search Availability By PinCode
    """
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/' \
          f'calendarByPin?pincode={pincode}&date={date}'

    try:
        request = requests.get(url, headers={})
        json_data = request.json()
        if request.status_code == 200:
            return json_data
        else:
            print('Error: ', str(json_data))
    except Exception as e:
        print('Exception: ', str(e))


def check_availability(district_id=None, pincode=None, date=None, age=None):    # noqa
    """
        Availability and Age Logic

        :param district_id: See list
        :param pincode:
        :param date: DD/MM/YYYY
        :param age: 45 or 18
        :return:
    """
    try:
        if district_id and pincode:
            raise ValueError('Pass only district_id or pincode')
        else:
            if district_id:
                response = search_by_district(district_id, date)
            elif pincode:
                response = search_by_pin(pincode, date)
            else:
                raise ValueError('No value for district_id or pincode')

        centers = response.get('centers')

        result = list()
        if centers:
            for center in centers:
                sessions = center.get('sessions')
                if sessions:
                    for session in sessions:
                        if session.get('available_capacity') > 0:
                            if age:
                                if session.get('min_age_limit') == age:
                                    result.append(center)
        return result
    except Exception as e:
        print('Exception: ', str(e))


def send_mail_smtp(from_email, to_email, msg_body):
    server = SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(from_email, to_email, msg_body)
    server.quit()


def send_mail(from_email, to_email, subject, content=''):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    message.attach(MIMEText(content, "html"))
    msg_body = message.as_string()

    send_mail_smtp(from_email, to_email, msg_body)


def format_json_data(data):
    if len(data) > 0:
        formatted_data = dict()
        for center in data:
            if not formatted_data.get(center['center_id']):
                formatted_data[center['center_id']] = dict()
                formatted_data[center['center_id']]['dates'] = list()

            formatted_data[center['center_id']]['name'] = center['name']
            formatted_data[center['center_id']]['state_name'] = center['state_name']  # noqa
            formatted_data[center['center_id']]['district_name'] = center['district_name']  # noqa
            formatted_data[center['center_id']]['block_name'] = center['block_name']  # noqa
            formatted_data[center['center_id']]['pincode'] = center['pincode']

            for session in center.get('sessions'):
                if not session.get('date') in formatted_data[center['center_id']]['dates']:  # noqa
                    formatted_data[center['center_id']]['dates'].append(session.get('date'))  # noqa

        return formatted_data
    else:
        return None
