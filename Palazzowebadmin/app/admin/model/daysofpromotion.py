#from app.admin.model.util import Fillter
#from datetime import date, datetime,timedelta
#class Autodeletedays(Fillter):
#    def __init__(self,days):
 #       super().__init__()
 #       self.days= days
 #       self.daysafter = self.deletedays()
 #   def deletedays(self):
 #       remove = []
 #       data = []
 #       days = [day for day in self.days.split(',')]
 #       for i in range(len(days)):
 #           if format4days(days[i]) < self.currentMonth:
 #               remove.append(days[i])
 #       for day in days:
 #           datetime_obj = datetime.strptime(day, "%m/%d/%Y")
 #           if day not in remove:
 #               data.append(str(datetime_obj.date().strftime('%Y/%m/%d')) )
 #       return data

#def format4days(day):
#    current_day = datetime.strptime(day, "%m/%d/%Y")
#    return current_day.month
        #     format_str = '%m/%d/%Y' # The format
    #     datetime_obj = datetime.strptime(day, format_str)
    #     data.append(str(datetime_obj.date().strftime('%Y/%m/%d')))
from app.admin.model.util import Fillter
from datetime import date, datetime,timedelta
class Autodeletedays(Fillter):
    def __init__(self,days):
        super().__init__()
        self.days= days
        self.daysafter = self.deletedays()
        self.getonlyday = self.getonlyday()
    def deletedays(self):
        remove = []
        data = []
        days = [day for day in self.days.split(',')]
        for i in range(len(days)):
            if format4days(days[i],"%m/%d/%Y") < self.currentMonth:
                remove.append(days[i])
        for day in days:
            datetime_obj = datetime.strptime(day, "%m/%d/%Y")
            if day not in remove:
                data.append(str(datetime_obj.date().strftime('%Y/%m/%d')) )
        return data
    def getonlyday(self):
        days = [formatonlyday(day,"%Y/%m/%d") for day in self.daysafter]
        return days
def format4days(day,formating):
    current_day = datetime.strptime(day,formating)
    return current_day.month
    
def formatonlyday(day,formating):
    current_day = datetime.strptime(day, formating)
    return current_day.day

        #     format_str = '%m/%d/%Y' # The format
    #     datetime_obj = datetime.strptime(day, format_str)
    #     data.append(str(datetime_obj.date().strftime('%Y/%m/%d')))
