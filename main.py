import pandas as pd
from dotenv import load_dotenv
import os
from playwright.sync_api import Page
from attendance_bot import AttendanceBot
from workday_checker import WorkdayChecker, is_weekend
from notification import Notification
import constants
import requests

load_dotenv ()

GREYTHR_ID = os.getenv('GREYTHR_ID')
GREYTHR_PASSWORD = os.getenv('GREYTHR_PASSWORD')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SHEETY_URL = os.getenv('SHEETY_URL')
ORG_CC = os.getenv('ORG_CC')
MANAGER_EMAIL = os.getenv('MANGER_EMAIL')
GREYTHR_URL = os.getenv('GREYTHR_URL')

response = requests.get(SHEETY_URL)
response.raise_for_status()

data = response.json()
content = pd.DataFrame(data["sheet1"])

notifier = Notification(email=EMAIL, password=PASSWORD, org_cc=ORG_CC, manager_email=MANAGER_EMAIL)
workday_checker = WorkdayChecker(content)
attendance_bot = AttendanceBot(greythr_id=GREYTHR_ID, greythr_password=GREYTHR_PASSWORD, page=Page, notifier=notifier, greythr_URL=GREYTHR_URL)

today_info = workday_checker.has_leave_today()

if not is_weekend():
    if workday_checker.should_mark_attendance():
        action = attendance_bot.get_action()
        if action == constants.CHECK_IN:
            attendance_bot.mark_login()
        else:
            attendance_bot.mark_logout()
    else:
        leave_type = today_info.get("leaveType")
        if leave_type == constants.SICK:
            notifier.send_sick_leave_mail()
        elif leave_type == constants.CASUAL:
            notifier.send_casual_leave_mail()
        else:
            print("leave today - attendance not marked")
else:
    print("It's weekend... attendance not marked")