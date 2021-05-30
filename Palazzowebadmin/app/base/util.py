# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
import calendar
from app import db
import hashlib, binascii, os
import base64
import os
from werkzeug.utils import secure_filename
import flask
from werkzeug.routing import BaseConverter, ValidationError
from app.admin.model.daysofpromotion import Autodeletedays

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass( password ):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def getimagespath(path):
    print(os.path.join(flask.request.host,path))
    return os.path.join(
        flask.request.host, path
        )

def saveimages(images):
    f = images
    save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/assets/img/calendar')
    filename = secure_filename(f.filename)
    f.save(os.path.join(save_path, filename))

    return getimagespath(os.path.join(
        'static/assets/img/calendar', filename))

def formatdate(days=str):
    data = []
    # for day in days.split(","):
    #     format_str = '%m/%d/%Y' # The format
    #     datetime_obj = datetime.strptime(day, format_str)
    #     data.append(str(datetime_obj.date().strftime('%Y/%m/%d')))
    formatdays = Autodeletedays(days)
    return formatdays.daysafter
    # return data
