from app import db, login_manager
from app.admin import blueprint
from app.base.forms import EventsForm, datepickerform, prioritizeForm
from app.base.models import Daysev, Devices, Events, Sevent
from flask import jsonify, render_template, redirect, request, url_for,make_response
from flask_login import login_required
from datetime import date
from app.base.util import add_months, saveimages
from flask.helpers import flash
from app.admin.model.devices import StatisticDevices
import flask

@blueprint.route('/promotions',methods=['GET','POST'])
@login_required
def promotions():
    number=10
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Events.idevent,Events.prioritize,Events.eventname,Events.urldetail,Events.status,
    Daysev.daysofevent,Daysev.expirydate,Daysev.datemodify).join(Daysev).order_by(Events.prioritize).paginate(page, per_page=number,
        error_out=False)
    form = prioritizeForm()
    promotion = pagination.items
    max = len(promotion)
    return render_template('promotions.html', events=promotion,max=max,pagination=pagination,form=form,segment='promotions')

@blueprint.route('/promotions/<int:id>/down',methods=['GET','POST'])
@login_required
def changepromopridown(id):
    try:
        promo = Events.query.get_or_404(id)
        old =      promo.prioritize
        new = old +1
        repromo = Events.query.filter_by(prioritize = new).first()
        promo.prioritize +=1
        repromo.prioritize-=1
        db.session.commit()
        return redirect(url_for('admin_blueprint.promotions'))
    except Exception as e:
        print(str(e))
        return render_template('page-500.html'), 500
@blueprint.route('/promotions/<int:id>/up',methods=['GET','POST'])
@login_required
def changepromopriup(id):
    try:
        promo = Events.query.get_or_404(id)
        old =      promo.prioritize
        new = old - 1
        repromo = Events.query.filter_by(prioritize = new).first()
        promo.prioritize -=1
        repromo.prioritize+=1
        db.session.commit()
        return redirect(url_for('admin_blueprint.promotions'))
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/promotions/<int:id>/changestatus',methods=['GET','POST'])
@login_required
def changepromostatus(id):
    try:
        data = request.form['status']
        promo = Events.query.get_or_404(id)
        events = db.session.query(Events.idevent,Events.prioritize,Events.eventname,Events.status,Daysev.daysofevent,Daysev.expirydate,Daysev.datemodify).join(Daysev).all()
        form = prioritizeForm()
        if data != '':
            if data =='y' and promo.status == True:
                promo.status = False
            elif data == 'y' and promo.status == False: 
                promo.status = True
            db.session.commit()
            db.session.remove()
            flash('The status of promotion has been change!')
            return redirect(url_for('admin_blueprint.promotions'))
        return render_template( 'promotions.html', events=events,form=form,segment='promotions')
    except:
        return render_template('page-500.html'), 500

@blueprint.route('/promotions/<int:id>/days',methods=['GET','POST'])
@login_required
def promotionsdays(id):
    try:
        promotions = Events.query.get_or_404(id)
        days = Daysev.query.filter_by(idevent = promotions.idevent).first()
        form = datepickerform()
        if form.validate_on_submit():
            data = request.form['days']
            days.daysofevent = data.replace(" ","")
            days.datemodify = date.today()
            days.status      = True
            days.expirydate = add_months(date.today(),2)
            db.session.commit()
            flash('Select days success!')
            return redirect(url_for('admin_blueprint.promotions'))
        return render_template('promotionsdays.html',days=days,form=form,event=promotions)
    except:
        return render_template('page-500.html'), 500

@blueprint.route('/promotions/add',methods=['GET','POST'])
@login_required
def add_promotion():
    form = EventsForm()
    if form.is_submitted():
        prilen = db.session.query(Events).count()

        event                   = Events(eventname = form.eventname.data,
                                        status      = True,
                                        urldetail   = form.urldetail.data,
                                        prioritize  = prilen +1)
        db.session.add(event)
        db.session.flush()
        eventdetail                             = Sevent(
                                                idevent                             =event.idevent, 
                                                entittle                            =form.ENTitle.data,
                                                cntittle                            =form.CNTitle.data,
                                                krtittle                            =form.KRTitle.data,
                                                endetail                            =form.ENdetail.data,
                                                cndetail                            =form.CNdetail.data,
                                                krdetail                            =form.KRdetail.data,
                                                endescription                       =form.ENdescription.data,
                                                cndescription                       =form.CNdescription.data,
                                                krdescription                       =form.KRdescription.data,
                                                enimagebase64                       =saveimages(form.ENimagebase64.data),
                                                cnimagebase64                       =saveimages(form.CNimagebase64.data),
                                                krimagebase64                       =saveimages(form.KRimagebase64.data),
                                                color                               =form.color.data,
                                                # prioritize                          =form.prioritize.data,
                                                singleevent                         =event)
        db.session.add(eventdetail)
        daysofevent = Daysev(idevent = event.idevent,daysofevent=date.today().strftime("%m/%d/%Y"))
        db.session.add(daysofevent)
        db.session.commit()
        flash('Promotion has been added!', 'success')
        return redirect(url_for('admin_blueprint.promotions'))
    return render_template( 'newpromotion.html',form=form,segment='newpromotion')

@blueprint.route('/promotions/<int:id>/edit',methods=['GET','POST'])
@login_required
def edit_promotion(id):
    form = EventsForm()
    events = Events.query.get_or_404(id)
    id = Sevent.query.filter_by(idevent=events.idevent).first().idsevent
    sevent = Sevent.query.get_or_404(id)
    if form.validate_on_submit():
        sevent.idevent          = events.idevent
        sevent.entittle         = form.ENTitle.data         
        sevent.cntittle         = form.CNTitle.data
        sevent.krtittle         = form.KRTitle.data
        sevent.endetail         = form.ENdetail.data
        sevent.cndetail         = form.CNdetail.data
        sevent.krdetail         = form.KRdetail.data
        sevent.endescription    = form.ENdescription.data
        sevent.cndescription    = form.CNdescription.data
        sevent.krdescription    = form.KRdescription.data
        sevent.enimagebase64    = saveimages(form.ENimagebase64.data)
        sevent.cnimagebase64    = saveimages(form.CNimagebase64.data)
        sevent.krimagebase64    = saveimages(form.KRimagebase64.data)
        sevent.color            = form.color.data
        events.eventname             = form.eventname.data
        events.urldetail        =form.urldetail.data
       # events.status           =form.status.data
        db.session.commit()
        flash('Update Promotion success!')
        return redirect(url_for('admin_blueprint.promotions'))
    form.ENTitle.data=sevent.entittle
    form.CNTitle.data=sevent.cntittle
    form.KRTitle.data=sevent.krtittle
    form.ENdetail.data=sevent.endetail
    form.CNdetail.data=sevent.cndetail
    form.KRdetail.data=sevent.krdetail
    form.ENdescription.data=sevent.endescription
    form.CNdescription.data=sevent.cndescription
    form.KRdescription.data=sevent.krdescription
    form.ENimagebase64.data=sevent.enimagebase64
    form.CNimagebase64.data=sevent.cnimagebase64
    form.KRimagebase64.data=sevent.krimagebase64
    form.color.data  =sevent.color
    form.eventname.data  =events.eventname 
    form.urldetail.data  = events.urldetail 
    return render_template( 'editpromotion.html',form=form,segment='editpromotion',id=events.idevent)

@blueprint.route("/promotions/<int:id>/delete",methods=['GET', 'POST'])
@login_required
def deletepromotion(id):
    try:
        events = Events.query.get_or_404(id)
        old = events.prioritize
        new = old +1
        if Events.query.filter_by(prioritize = new).first() is not None:
            repromo = Events.query.filter_by(prioritize = new).first()
            repromo.prioritize-=1
        db.session.delete(events)
        db.session.commit()

        return redirect(url_for('admin_blueprint.promotions'))
    except Exception as e:
        print(str(e))
        return render_template('page-500.html'), 500

# @blueprint.route('/option10')
# @login_required
# def show_option_10():
#     resp = make_response(redirect(url_for('admin_blueprint.promotions')))
#     host = flask.request.host

#     resp.delete_cookie('choose20', path='/' , domain=None)
#     resp.delete_cookie('choose30', path='/' , domain=None)
#     return resp

# @blueprint.route('/option20')
# @login_required
# def show_option_20():
#     resp = make_response(redirect(url_for('admin_blueprint.promotions')))
#     host = flask.request.host
#     resp.delete_cookie('choose30', path='/' , domain=None)
#     resp.set_cookie('choose20', '', expires=0)
#     return resp

# @blueprint.route('//option30')
# @login_required
# def show_option_30():
#     resp = make_response(redirect(url_for('admin_blueprint.promotions')))
#     host = flask.request.host
#     resp.delete_cookie('choose20', path='/' , domain=None)
#     resp.set_cookie('choose30', '', max_age=1 * 60 * 60 * 24)
#     return resp
#--------------------------------------customer----------------------------------
# https://sontran.loca.lt/
@blueprint.route("/statistic",methods=['GET', 'POST'])
@login_required
def statistic():
    try:
        st = StatisticDevices()
        return render_template('customers.html',st=st,segment='statistic')
    except Exception as e:
        print(str(e))
        return render_template('page-500.html'), 500
