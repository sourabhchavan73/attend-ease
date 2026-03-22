from email.message import EmailMessage
import smtplib
import constants

class Notification:
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.org_cc = kwargs.get('org_cc')
        self.manager_email = kwargs.get('manager_email')

    def send_email(self, message):
        msg = EmailMessage()
        msg["Subject"] = "AttendEase Bot - Attendance Update"
        msg["From"] = "AttendEase Bot"
        msg["To"] = self.email
        msg.set_content(message)

        with smtplib.SMTP(constants.SERVER, 587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.send_message(msg)

    def send_success(self, message):
        self.send_email(message)

    def send_failure(self, message):
        self.send_email(message)

    def send_sick_leave_mail(self):
        with open('./email-templates/sick-leave') as file:
            content = file.read()
        msg = EmailMessage()
        msg["Subject"] = "Out Sick Today"
        msg["From"] = self.email
        msg["To"] = self.manager_email
        cc_list = [e.strip() for e in self.org_cc.split(",") if e.strip()]
        msg["Cc"] = ", ".join(cc_list)
        msg.set_content(content)
        with smtplib.SMTP(constants.SERVER, 587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.send_message(msg)

    def send_casual_leave_mail(self):
        with open('./email-templates/casual-leave') as file:
            content = file.read()
        msg = EmailMessage()
        msg["Subject"] = "Casual Leave – Today"
        msg["From"] = self.email
        msg["To"] = self.manager_email
        cc_list = [e.strip() for e in self.org_cc.split(",") if e.strip()]
        msg["Cc"] = ", ".join(cc_list)
        msg.set_content(content)
        with smtplib.SMTP(constants.SERVER, 587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.send_message(msg)

