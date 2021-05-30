# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String,Text,DateTime

from app import db, login_manager

from app.base.util import hash_pass

from datetime import datetime
class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String, unique=True)
    email = db.Column(String, unique=True)
    password = db.Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Events(db.Model, UserMixin):
    idevent                     = db.Column(db.Integer, primary_key=True)
    eventname                   = db.Column(db.Text, nullable=False)
    status                      = db.Column(db.Boolean, default=True, nullable=False)
    urldetail                   = db.Column(db.Text, nullable=False)
    prioritize                  = db.Column(db.Integer, nullable=True)
    singleEvent                 =db.relationship('Sevent', backref='singleevent',cascade="all,delete", lazy='dynamic')
    statistical                 = db.relationship('statistical', backref='eventsofstatistic', lazy=True)
    # EventssofDay                = db.relationship('EventssofDay', backref='eventsofday', lazy=True)
    daysev                 = db.relationship('Daysev', backref='days',cascade="all,delete", lazy=True)
    def __str__(self):
        return super().__str__(idevent,eventname,status)
class Sevent(db.Model, UserMixin):
    idsevent                    = db.Column(db.Integer, primary_key=True)
    idevent                     = db.Column(db.Integer, db.ForeignKey('events.idevent', ondelete='CASCADE'), nullable=False)
    entittle                    = db.Column(db.Text, nullable=True)
    cntittle                    = db.Column(db.Text, nullable=True)
    krtittle                    = db.Column(db.Text, nullable=True)
    endetail                    = db.Column(db.Text, nullable=True)
    cndetail                    = db.Column(db.Text, nullable=True)
    krdetail                    = db.Column(db.Text, nullable=True)
    endescription               = db.Column(db.Text, nullable=True)
    cndescription               = db.Column(db.Text, nullable=True)
    krdescription               = db.Column(db.Text, nullable=True)
    enimagebase64               = db.Column(db.Text, nullable=True)
    cnimagebase64               = db.Column(db.Text, nullable=True)
    krimagebase64               = db.Column(db.Text, nullable=True)
    color                       = db.Column(db.Text, nullable=True)
    prioritize                  = db.Column(db.Integer, nullable=True)
    def __str__(self):
        return super().__str__(idsevent,idevent,entittle,cntittle,krtittle,
                                                            endetail,     
                                                            cndetail     
                                                            ,krdetail     
                                                            ,endescription
                                                            ,cndescription
                                                            ,krdescription
                                                            ,enimagebase64
                                                            ,cnimagebase64
                                                            ,krimagebase64
                                                            ,color        
                                                            ,prioritize   )
class Daysev(db.Model, UserMixin):
    daysofeventid                = db.Column(db.Integer, primary_key=True)
    idevent                     = db.Column(db.Integer, db.ForeignKey('events.idevent',
                                                                     ondelete='CASCADE'), nullable=False)
    daysofevent                  = db.Column(db.Text, nullable=False)
    datecreate                   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expirydate                   = db.Column(db.DateTime, nullable=True)
    datemodify                    = db.Column(db.DateTime, nullable=True)
    modifyby                     = db.Column(db.Text, nullable=True)
    status                       = db.Column(db.Boolean, default=False)
    def __str__(self):
        return super().__str__(daysofeventid,idevent,daysofevent)
class EventssofDay(db.Model, UserMixin):
    eventssofdayid              = db.Column(db.Integer, primary_key=True)

    dayCalendar                 = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prioritizeEvent             = db.Column(db.Integer, db.ForeignKey('events.idevent',
                                                                 ondelete='CASCADE'), nullable=False)
    EventssofDay                = db.Column(db.Text, nullable=False)



class Footerdata(db.Model, UserMixin):
    f_id               = db.Column(db.Integer, primary_key=True)
    f_name                      = db.Column(db.Text, nullable=False)
    f_value                      = db.Column(db.Text, nullable=False,default = '0')
    status                       = db.Column(db.Boolean, default=True)
    modifyday                    = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    modifyby                     = db.Column(db.Text, nullable=True)
    def __str__(self):
        return super().__str__(f_name,f_value)


class Devices(db.Model, UserMixin):
    devicesid                   = db.Column(db.Integer, primary_key=True)
    fcmtoken                    = db.Column(db.Text, nullable=False)
    datecreate                   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastmodify                   = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    countjoin                    = db.Column(db.Integer, nullable=False,default=0)
    statistical                 = db.relationship('statistical', backref='devices', lazy=True)

class statistical(db.Model, UserMixin):
    statisticalid                   = db.Column(db.Integer, primary_key=True)
    devicesid                   = db.Column(db.Integer, db.ForeignKey('devices.devicesid',
                                                                 ondelete='CASCADE'), nullable=False)
    idevent                     = db.Column(db.Integer, db.ForeignKey('events.idevent',
                                                                 ondelete='CASCADE'), nullable=False)
    ncount                      = db.Column(db.Integer, nullable=False,default=0)

class roles(db.Model, UserMixin):

    roleid                      = db.Column(db.Integer, primary_key=True)
    name                        = db.Column(db.Text, nullable=False,default = 'CUSTOMER')
    detail                      = db.Column(db.Text, nullable=False,default = 'Quyền truy cập mobile')
    position                    = db.Column(db.Integer, primary_key=True,default = 'Client')
    acronym                     = db.Column(db.Text, nullable=False,default='G')
    permission                  = db.Column(db.Text, nullable=False,default='guest')
    status                      = db.Column(db.Boolean, nullable=False,default=True)
    usersroles                  = db.relationship('usersroles', backref='roles', lazy=True)

class usersroles(db.Model, UserMixin):
    usersrolesid                  = db.Column(db.Integer, primary_key=True)
    roleid                      = db.Column(db.Integer, db.ForeignKey('roles.roleid',
                                                                 ondelete='CASCADE'), nullable=False)
    userid                      = db.Column(db.Integer, db.ForeignKey('users.userid',
                                                                 ondelete='CASCADE'), nullable=False)
    description                 = db.Column(db.Text, nullable=False)
    status                      = db.Column(db.Text, nullable=False)
