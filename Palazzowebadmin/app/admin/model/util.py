from datetime import date, datetime,timedelta
import calendar
class Fillter:
    def __init__(self):
        self.currentDaytime = datetime.now()
        self.currentDay = datetime.now().day
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year
        self.today      = datetime.strptime(datetime.now().strftime("%m/%d/%y"), "%m/%d/%y")
        self.day7ago      = self.day7_ago()
        self.day30ago     = self.day30_ago()
    def day7_ago(self):

        end_date = self.today - timedelta(days=7)
        return end_date
    def day30_ago(self):
        end_date = self.today - timedelta(days=30)
        return end_date