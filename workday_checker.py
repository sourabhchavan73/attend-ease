from datetime import datetime

def is_weekend():
    today = datetime.today()
    return today.weekday() >= 5

class WorkdayChecker:
    def __init__(self, holidays_df):
        self.holidays = holidays_df

    def has_leave_today(self):
        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day

        for index, row in self.holidays.iterrows():
            if row['year'] == year and row['month'] == month and row['day'] == day:
                return row
        return None

    def should_mark_attendance(self):
        return self.has_leave_today() is None
