from datetime import datetime, time
from playwright.sync_api import sync_playwright, expect
import constants
import my_selectors as selectors
import labels

class AttendanceBot:
    def __init__(self, **kwargs):
        self.email = kwargs.get("greythr_id")
        self.password = kwargs.get("greythr_password")
        self.page = kwargs.get("page")
        self.notifier = kwargs.get("notifier")
        self.greythr_url = kwargs.get("greythr_URL")

    def get_action(self):
        now = datetime.now().time()
        if now < time(13, 0):
            return constants.CHECK_IN
        else:
            return constants.CHECK_OUT

    def perform_action(self, action_name):
        try:
            with sync_playwright() as p:
                print("Launching browser...")

                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                print("Opening page...")
                page.goto(self.greythr_url)

                # Login
                page.get_by_role(selectors.textbox, name=labels.login_id).fill(self.email)
                page.get_by_role(selectors.textbox, name=labels.password).fill(self.password)
                page.get_by_role(selectors.button, name=labels.login).click()

                # Dynamic button (Sign In / Sign Out)
                action_button = page.get_by_role(selectors.button, name=action_name)
                expect(action_button).to_be_visible(timeout=180000)

                action_button.click()
                message = (f"Hi,"
                           f"\n"
                           f"{action_name} successful for - {datetime.now().strftime('%d %b %Y')}")

                self.notifier.send_success(message)

        except Exception as e:
            message = (f"Hi,"
                       f"\n"
                       f"failed to {action_name} - {datetime.now().strftime('%d %b %Y')} \n {e}")

            self.notifier.send_failure(message)

    def mark_login(self):
        self.perform_action("Sign In")

    def mark_logout(self):
        self.perform_action("Sign Out")