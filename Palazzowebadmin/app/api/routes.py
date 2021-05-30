from app.api import blueprint
from app.base.models import Daysev, Devices, Events, Footerdata, Sevent
from app import db
from flask_login import login_required

from app.base.util import formatdate
import sys
from flask import jsonify,redirect,url_for,render_template,request
import logging
import requests
import json
from datetime import date,datetime
from app import csrf
from app.admin.model.util import Fillter
from app.api.model import getname

from app.admin.model.daysofpromotion import Autodeletedays, format4days, formatonlyday
csrf.exempt(blueprint)
@blueprint.route('/api/promotions',methods=['GET','POST'])
def devices_post():
    try:
        if request.method == 'POST':

            events = db.session.query(
                Events.idevent,
                Events.eventname,
                Events.status,
                Daysev.daysofevent,
                Sevent.entittle,
                Sevent.cntittle,
                Sevent.krtittle,
                Sevent.endetail,
                Sevent.cndetail,
                Sevent.krdetail,
                Sevent.endescription,
                Sevent.cndescription,
                Sevent.krdescription,
                Sevent.enimagebase64,
                Sevent.cnimagebase64,
                Sevent.krimagebase64,
                Sevent.color, 
                Events.prioritize,
                Events.urldetail
                
            ).join(Daysev).join(Sevent).all()
            data = []

            for event in events:
                dat2 = {
                    'event_id' :            event.idevent,
                    'event_name':           event.eventname,
                    'event_status':         event.status,
                    'event_days'        :   formatdate(event.daysofevent),
                    'event_en_tittle'     : event.entittle, 
                    'event_cn_tittle'     : event.cntittle, 
                    'event_kr_tittle'     : event.krtittle, 
                    'event_en_detail'     : event.endetail,
                    'event_cn_detail'     : event.cndetail, 
                    'event_kr_detail'     : event.krdetail, 
                    'event_en_description': event.endescription, 
                    'event_cn_description': event.cndescription, 
                    'event_kr_description': event.krdescription, 
                    'event_color'        :  event.color, 
                    'event_prioritize'   :  event.prioritize,
                    'event_enimage':      event.enimagebase64.replace("localhost:5000","https://sontran.loca.lt"),
                    'event_cnimage':      event.cnimagebase64.replace("localhost:5000","https://sontran.loca.lt"),
                    "event_krimage":      event.krimagebase64.replace("localhost:5000","https://sontran.loca.lt"),
                    "event_urldetail":      event.urldetail
                }
                data.append(dat2)
            print(sys.getsizeof(data)) 
            return jsonify({"success": True,"data": data}), 200
        else:
            return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500

@blueprint.route("/api/jackpot",methods=['GET','POST'])
def jackpot_info():
    try:
        if request.method == 'POST':
            jt = Footerdata.query.all()
            jackpot = []
            for t in jt:
                jackpot.append(
                    {'id':t.f_id,
                    'j_name':t.f_name,
                    'j_value':t.f_value,
                    'j_status':t.status,
                    'unit':'$'}
                )
            return jsonify({"success": True,"jackpot": jackpot}), 200
        else:
            return render_template('page-404.html'), 404
    except Exception as e:
        return render_template('page-500.html'), 500

@blueprint.route("/api/priority",methods=['GET','POST'])
def prioritize():
    try:
        if request.method == 'POST':
            pr = db.session.query(Events.eventname,Events.prioritize,Sevent.entittle,Sevent.krtittle,Sevent.cntittle).join(Events).all()
            priority = []
            for p in pr:
                priority.append(
                    {'promotion_name':p.eventname,
                    'priority':p.prioritize,
                    'promo_entitle':p.entittle,
                    'promo_krtitle':p.krtittle,
                    'promo_cntitle':p.cntittle}
                )
            return jsonify({"success": True,"data": priority}), 200
    except Exception as e:
        return render_template('page-500.html'), 500

@blueprint.route("/api/devices/init",methods=['POST'])
def initdevices():
    try:
        if request.method == 'POST':
            fcmtoken = request.values['fcmtoken']
            checkexists = Devices.query.filter_by(fcmtoken=fcmtoken).first() is not None
            if checkexists:
                oldevices = Devices.query.filter_by(fcmtoken=fcmtoken).first()
                oldevices.lastmodify  = date.today()
                oldevices.countjoin += 1
                db.session.commit()
            else:
                devices = Devices(
                    fcmtoken    = fcmtoken,
                    datecreate  = date.today(),
                    lastmodify  = date.today(),
                    countjoin   = 1
                    )
                db.session.add(devices)
                db.session.commit()
            return jsonify({"success": True}), 200
        else:
            return render_template('page-404.html'), 404
    except Exception as e:
        return render_template('page-500.html'), 500


@blueprint.route('/api/desciptions',methods=['GET','POST'])
def desciptions():
    try:
        if request.method == 'POST':
            data = request.values['id']
            listdata = json.loads(data)
            events = db.session.query(
            Events.idevent,
            Sevent.endescription,
            Sevent.cndescription,
            Sevent.krdescription
          
        ).join(Sevent).filter(Events.idevent.in_(listdata)).all()
            data = []
            for event in events:
                dat2 = {
                    'event_id' :            event.idevent,
                    'event_en_description': event.endescription, 
                    'event_cn_description': event.cndescription, 
                    'event_kr_description': event.krdescription
                }
                data.append(dat2)
            print(sys.getsizeof(data))
            return jsonify({"success": True,"data": data}), 200
        else:
            return render_template('page-404.html'), 404
    except Exception as e:
        return render_template('page-500.html'), 500



@blueprint.route('/api/webengdata',methods=['GET','POST'])
def webeng_data():
    try:
        if request.method == 'POST':

            events = db.session.query(
                Events.idevent,
                Events.eventname,
                Events.status,
                Daysev.daysofevent,
                Sevent.entittle,
                Sevent.cntittle,
                Sevent.krtittle,
                Sevent.endetail,
                Sevent.cndetail,
                Sevent.krdetail,
                Sevent.endescription,
                Sevent.cndescription,
                Sevent.krdescription,
                Sevent.enimagebase64,
                Sevent.cnimagebase64,
                Sevent.krimagebase64,
                Sevent.color,
                Events.prioritize,
                Events.urldetail

            ).join(Daysev).join(Sevent).all()
            list_promotion = []
            promotions = []
            titles = []
            info_promotions = []


            for event in events:
                if event.status:
                    formatdays = Autodeletedays(event.daysofevent)
                    list_promotion.append({
                        'name': getname(event.eventname),
                        'color': event.color,
                        'slug': event.idevent
                    })
                    promotions.append({
                        'name': getname(event.eventname),
                        'slug': event.idevent,
                        'day': formatdays.getonlyday,
                        'endetail': event.endetail,
                        'krdetail': event.cndetail,
                        'cndetail': event.krdetail,
                        'color': event.color,
                    })
                    titles.append({
                        'title': event.entittle,
                        'day': [4, 8, 9, 12],
                        'day_in_week': [],
                        'time': '07:00'
                            })
                    info_promotions.append({
                        'title': getname(event.eventname),
                        'slug': event.idevent,
                        'info': """
                        <div style="text-align: left">
                            <p>It is a mid-week EXTRA BONUS due to the level rush journey, Rush-up your level today from any level as
                            the Level rush level’s and enjoy the instant EXTRA BONUS right away. </p>
                            <p>Example: If you in Level 2 as per today and you rush the required point today to Level 3 or above level,
                            then you get EXTRA BONUS right away as the level bonus allocated.</p>
                        </div>
                        """
                        })
            promotions.append({
                'name': "ALL",
                'slug': 'all',
                'day': [],
                'color': '#FF5733'
            })
            list_promotion.append({
                'name': "ALL",
                'color': '#FF5733',
                'slug': 'all'
                })
            engdata = {
                'list_promotion':list_promotion,
                'promotions':promotions,
                'titles':titles,
                'info_promotions':info_promotions,
                'term': '- Term & Condition Apply -'
            }
            return jsonify({"success": True,"engdata": engdata}), 200
        else:
            return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500

@blueprint.route("/api/gettitle",methods=['GET','POST'])
def gettitle():
    try:
        if request.method == 'POST':
            pr = db.session.query(Events.idevent,Events.eventname,Events.prioritize,Sevent.entittle,Sevent.krtittle,Sevent.cntittle,Daysev.daysofevent).join(Daysev).join(Sevent).all()
            x= y = len(pr)
            for p in pr:
                formatdays = Autodeletedays(p.daysofevent)
                days = formatdays.daysafter
                for day in days:
                    if format4days(day,"%Y/%m/%d") == formatdays.currentMonth and formatonlyday(day,"%Y/%m/%d") == formatdays.currentDay:
                        if p.prioritize < y:
                            x = p.idevent
                            y = p.prioritize
                            priority = {
                            'promo_entitle':p.entittle[5:],
                            'promo_krtitle':p.krtittle[5:],
                            'promo_cntitle':p.cntittle[5:],
                            'time': p.entittle[0:4]}
                    if p.idevent == x:
                        break
            return jsonify({"success": True,"title": priority}), 200
    except Exception as e:
        return render_template('page-500.html'), 500
