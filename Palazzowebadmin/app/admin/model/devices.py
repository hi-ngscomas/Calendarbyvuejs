
from app import db
from app.base.models import Devices
from sqlalchemy import extract, and_



from app.admin.model.util import Fillter

class StatisticDevices(Fillter):
    def __init__(self):
        super().__init__()
        devicesdb   = Devices.query.all()
        self.total  = len(devicesdb)
        self.devicesinmonth = self.totalofmonth()
        self.returntoday  = self.devicesreturntoday()
        self.return7day  = self.devicesreturn7day()
        self.notreturn30day  = self.devicesnotreturn30day()
        self.notreturn7day  = self.devicesnotreturn7day()

    def totalofmonth(self):
        devicesmonth = Devices.query.filter(and_(
            extract('year', Devices.datecreate) == self.currentYear,
            extract('month', Devices.datecreate) == self.currentMonth)).all()
        return len(devicesmonth)

    def devicesreturntoday(self):
        devicesdate = Devices.query.filter(and_(
            extract('year', Devices.lastmodify) == self.currentYear,
            extract('month', Devices.lastmodify) == self.currentMonth,
            extract('day', Devices.lastmodify) == self.currentDay)).all()
        return len(devicesdate)

    def devicesreturn7day(self):
        counts = len(db.session.query(Devices).filter(
        and_(Devices.lastmodify <= self.currentDaytime, Devices.lastmodify >= self.day7ago)).all()) 
        return counts
    def devicesnotreturn30day(self):
        counts = int(self.total) - len(db.session.query(Devices).filter(
        and_(Devices.lastmodify <= self.currentDaytime, Devices.lastmodify >= self.day30ago)).all()) 
        return counts
    def devicesnotreturn7day(self):
        counts =int(self.total) - len(db.session.query(Devices).filter(
        and_(Devices.lastmodify <= self.currentDaytime, Devices.lastmodify >= self.day7ago)).all()) 
        return counts
        

