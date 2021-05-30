from app import db, login_manager
from app.jackpot import blueprint
from app.base.forms import footerForm
from app.base.models import Footerdata
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import login_required
from flask.helpers import flash
from datetime import date
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import json
# ----------------------------- Jackpot info  -----------------------------#

@blueprint.route("/jackpot",methods=['GET', 'POST'])
@login_required
def jackpotinfo():
    jackpots= Footerdata.query.order_by(Footerdata.f_id).all()
    form = footerForm()
    return render_template('jackpots.html', jackpots = jackpots,form=form, segment='jackpots')

@blueprint.route("/jackpot/add",methods=['GET', 'POST'])
@login_required
def addjackpotinfo():
    name = request.form['name']
    value = request.form['value']
    jackpot                   = Footerdata(f_name = name,
                                            f_value = value,
                                            modifyby    = current_user.username
                                            )
    db.session.add(jackpot)
    db.session.flush()
    db.session.commit()
    flash('Data has been added!', 'success')
    return redirect(url_for('jackpot_blueprint.jackpotinfo'))

@blueprint.route("/jackpot/<int:id>/edit",methods=['GET', 'POST'])
@login_required
def editjackpotinfo(id):
    jackpot= Footerdata.query.get_or_404(id)
    name = request.form['name']
    value = request.form['value']
    jackpot.f_name = name
    jackpot.f_value = value
    jackpot.modifyday = date.today()
    jackpot.modifyby = current_user.username
    db.session.add(jackpot)
    db.session.commit()
    flash('The element has been updated.')
    return redirect(url_for('jackpot_blueprint.jackpotinfo'))

@blueprint.route("/jackpot/<int:id>/delete",methods=['GET', 'POST'])
@login_required
def deletejackpotinfo(id):
    jackpot=  Footerdata.query.get_or_404(id)
    db.session.delete(jackpot)
    db.session.commit()
    return redirect(url_for('jackpot_blueprint.jackpotinfo'))

@blueprint.route('/jackpot/<int:id>/changestatus',methods=['GET','POST'])
@login_required
def changejackpotstatus(id):
    try:
        data = request.form['status']
        jacpot = Footerdata.query.get_or_404(id)
        if data != '':
            if data =='y' and jacpot.status == True:
                jacpot.status = False
            elif data == 'y' and jacpot.status == False: 
                jacpot.status = True
            db.session.commit()
            db.session.remove()
            return redirect(url_for('jackpot_blueprint.jackpotinfo'))
        else:
            return render_template('page-500.html'), 500
    except:
        return render_template('page-500.html'), 500

@blueprint.route("/jackpot/update",methods=['GET', 'POST'])
def updatejackpot():
    if request.method == 'POST':
        id = request.values['id']
        value = request.values['value']
        json.loads(id)
        jackpot= Footerdata.query.get_or_404(id)
        jackpot.f_value = value
        jackpot.modifyday = date.today()
        jackpot.modifyby = 'auto requests'
        db.session.add(jackpot)
        db.session.commit()
        return jsonify({"success": True}), 200
