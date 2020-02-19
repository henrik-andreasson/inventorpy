from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Service, Location, User
from app.modules.server.models import Server
from app.modules.hsm.models import HsmDomain, HsmPed, HsmPin, HsmBackupUnit, \
    HsmPciCard
from app.modules.hsm.forms import HsmDomainForm, HsmPedForm, HsmPinForm, \
    HsmPciCardForm, HsmBackupUnitForm
from rocketchat_API.rocketchat import RocketChat
from flask_babel import _
import pprint

@bp.route('/hsm/domain/add', methods=['GET', 'POST'])
@login_required
def hsm_domain_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmDomainForm(formdata=request.form)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.name, service.name)]

    else:
        form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(name=form.service.data).first()

        hsmdomain = HsmDomain(name=form.name.data)
        hsmdomain.service = service
        db.session.add(hsmdomain)
        db.session.commit()
        flash(_('New HSM Domain is now posted!'))

        return redirect(url_for('main.index'))

    else:

        hsmdomains = HsmDomain.query.order_by(HsmDomain.name.desc()).limit(10)
        return render_template('hsm.html', title=_('HSM'),
                               form=form, hsmdomains=hsmdomains)


@bp.route('/hsm/domain/edit/', methods=['GET', 'POST'])
@login_required
def hsm_domain_edit():

    domainid = request.args.get('domain')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_domain_delete', domain=domainid))

    hsmdomain = HsmDomain.query.get(domainid)

    form = HsmDomainForm(obj=hsmdomain)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.name, service.name)]

    else:
        form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    if hsmdomain is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(name=form.service.data).first()
        hsmdomain.name = form.name.data
        hsmdomain.service = service

        db.session.commit()
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/domain/list/', methods=['GET', 'POST'])
@login_required
def hsm_domain_list():

    page = request.args.get('page', 1, type=int)

    hsmdomains = HsmDomain.query.order_by(HsmDomain.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.hsm_domain_list', page=hsmdomains.next_num) \
        if hsmdomains.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmdomains.prev_num) \
        if hsmdomains.has_prev else None

    return render_template('hsm.html', title=_('HSM Domains'),
                           hsmdomains=hsmdomains.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/hsm/domain/delete/', methods=['GET', 'POST'])
@login_required
def hsm_domain_delete():

    domainid = request.args.get('domain')
    hsmdomain = HsmDomain.query.get(domainid)

    if hsmdomain is None:
        flash(_('HSM Domain was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'HSM Domain deleted: %s %s' % (hsmdomain.name,
                                                 hsmdomain.service.name)
    db.session.delete(hsmdomain)
    db.session.commit()
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/ped/add', methods=['GET', 'POST'])
@login_required
def hsm_ped_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPedForm()
    print("ped input: %s-%s-%s-%s" % (form.hsmdomain.data,form.user.data,form.keyno.data,form.keysn.data))

    form.hsmdomain.choices = [(h.name, h.name) for h in HsmDomain.query.all()]
    form.user.choices = [(u.username, u.username) for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.filter_by(name=form.hsmdomain.data).first()
        user = User.query.filter_by(username=form.user.data).first()

        hsmped = HsmPed(keyno=form.keyno.data,
                        keysn=form.keysn.data)
        hsmped.hsmdomain = hsmdomain
        hsmped.user = user
        db.session.add(hsmped)
        db.session.commit()
        flash(_('New HSM PED is now posted!'))

        return redirect(url_for('main.index'))

    else:

        hsmpeds = HsmPed.query.order_by(HsmPed.keysn.desc()).limit(10)
        return render_template('hsm.html', title=_('HSM'),
                               form=form, hsmpeds=hsmpeds)


@bp.route('/hsm/ped/edit/', methods=['GET', 'POST'])
@login_required
def hsm_ped_edit():

    pedid = request.args.get('ped')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_ped_delete', ped=pedid))

    print("pedid: %s" % pedid)
    hsmped = HsmPed.query.get(pedid)
    if hsmped is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    form = HsmPedForm(obj=hsmped)

    form.hsmdomain.choices = [(h.name, h.name) for h in HsmDomain.query.all()]
    form.user.choices = [(u.username, u.username) for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.filter_by(name=form.hsmdomain.data).first()
        user = User.query.filter_by(username=form.user.data).first()
        hsmped.keyno = form.keyno.data
        hsmped.keysn = form.keysn.data
        hsmped.hsmdomain = hsmdomain
        hsmped.user = user
        db.session.commit()
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/ped/list/', methods=['GET', 'POST'])
@login_required
def hsm_ped_list():

    page = request.args.get('page', 1, type=int)

    hsmpeds = HsmPed.query.order_by(HsmPed.keysn).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.hsm_ped_list', page=hsmpeds.next_num) \
        if hsmpeds.has_next else None
    prev_url = url_for('main.hsm_ped_list', page=hsmpeds.prev_num) \
        if hsmpeds.has_prev else None

    return render_template('hsm.html', title=_('HSM Domains'),
                           hsmpeds=hsmpeds.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/hsm/ped/delete/', methods=['GET', 'POST'])
@login_required
def hsm_ped_delete():

    pedid = request.args.get('ped')
    hsmped = HsmPed.query.get(pedid)

    if hsmped is None:
        flash(_('HSM PED was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'HSM PED deleted: %s %s' % (hsmped.keyno,
                                              hsmped.hsmdomain.name)
    db.session.delete(hsmped)
    db.session.commit()
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pin/add', methods=['GET', 'POST'])
@login_required
def hsm_pin_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPinForm()
    peds = []
    for h in HsmPed.query.all():
        pedstr = "%s-%s-%s-%s-%s" % (h.id, h.hsmdomain.name, h.keyno, h.keysn, h.user.username)
        ped = (h.id, pedstr)
        peds.append(ped)

    form.ped.choices = peds
    if request.method == 'POST' and form.validate_on_submit():
        hsmped = HsmPed.query.get(form.ped.data)
#        safe = HsmPed.query.filter_by(id=form.safe.data).first()
        hsmpin = HsmPin(safe=form.safe.data)
        hsmpin.ped = hsmped
#        hsmpin.safe = safe
        db.session.add(hsmpin)
        db.session.commit()
        flash(_('New HSM PIN is now posted!'))

        return redirect(url_for('main.index'))

    else:

        hsmpins = HsmPin.query.all()
        return render_template('hsm.html', title=_('HSM'),
                               form=form, hsmpins=hsmpins)


@bp.route('/hsm/pin/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pin_edit():

    pinid = request.args.get('pin')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pin_delete', pin=pinid))

    hsmpin = HsmPin.query.get(pinid)

    form = HsmPinForm(obj=hsmpin)

    if hsmpin is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    peds = []
    for h in HsmPed.query.all():
        pedstr = "%s-%s-%s-%s-%s" % (h.id, h.hsmdomain.name, h.keyno, h.keysn, h.user.username)
        ped = (h.id, pedstr)
        peds.append(ped)

    form.ped.choices = peds

    if request.method == 'POST' and form.validate_on_submit():
        hsmped = HsmPed.query.get(form.ped.data)
#        safe = HsmPed.query.filter_by(id=form.safe.data).first()
#        hsmpin.safe = safe
        hsmpin.safe = form.safe.data
        hsmpin.ped = hsmped
        db.session.commit()
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/pin/list/', methods=['GET', 'POST'])
@login_required
def hsm_pin_list():

    page = request.args.get('page', 1, type=int)

    hsmpins = HsmPin.query.order_by(HsmPin.id).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.hsm_pin_list', page=hsmpins.next_num) \
        if hsmpins.has_next else None
    prev_url = url_for('main.hsm_pin_list', page=hsmpins.prev_num) \
        if hsmpins.has_prev else None

    return render_template('hsm.html', title=_('HSM Domains'),
                           hsmpins=hsmpins.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/hsm/pin/delete/', methods=['GET', 'POST'])
@login_required
def hsm_pin_delete():

    pinid = request.args.get('pin')
    hsmpin = HsmPin.query.get(pinid)

    if hsmpin is None:
        flash(_('HSM PED was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'HSM PED deleted: %s %s %s' % (hsmpin.ped.keyno,
                                                 hsmpin.ped.keysn,
                                                 hsmpin.ped.hsmdomain.name)
    db.session.delete(hsmpin)
    db.session.commit()
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pcicard/add', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPciCardForm()

    form.hsmdomain.choices = [(h.name, h.name) for h in HsmDomain.query.all()]
    form.server.choices = [(s.id, s.hostname) for s in Server.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.filter_by(name=form.hsmdomain.data).first()
        server = Server.query.filter_by(id=form.server.data).first()
        hsmpcicard = HsmPciCard(serial=form.serial.data,
                                model=form.model.data,
                                manufacturedate=form.manufacturedate.data,
                                fbno=form.fbno.data)
        hsmpcicard.hsmdomain = hsmdomain
    #    hsmpcicard.safe = safe
        hsmpcicard.server = server
        db.session.add(hsmpcicard)
        db.session.commit()
        flash(_('New HSM PCI is now posted!'))

        return redirect(url_for('main.index'))

    else:

        hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.hsmdomain.desc()).limit(10)
        return render_template('hsm.html', title=_('HSM'),
                               form=form, hsmpcicards=hsmpcicards)


@bp.route('/hsm/pcicard/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_edit():

    pcicardid = request.args.get('pcicard')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pcicard_delete', pcicard=pcicardid))

    hsmpcicard = HsmPciCard.query.get(pcicardid)

    form = HsmPciCardForm(obj=hsmpcicard)
    form.hsmdomain.choices = [(h.name, h.name) for h in HsmDomain.query.all()]
    form.user.choices = [(u.username, u.username) for u in User.query.all()]

    if hsmpcicard is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(name=form.service.data).first()
        hsmpcicard.name = form.name.data
        hsmpcicard.service = service

        db.session.commit()
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/pcicard/list/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_list():

    page = request.args.get('page', 1, type=int)

    hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.keysn).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.hsm_domain_list', page=hsmpcicards.next_num) \
        if hsmpcicards.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmpcicards.prev_num) \
        if hsmpcicards.has_prev else None

    return render_template('hsm.html', title=_('HSM Domains'),
                           hsmpcicards=hsmpcicards.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/hsm/pcicard/delete/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_delete():

    pcicardid = request.args.get('pcicard')
    hsmpcicard = HsmPciCard.query.get(pcicardid)

    if hsmpcicard is None:
        flash(_('HSM PED was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'HSM PED deleted: %s %s' % (hsmpcicard.keyno,
                                              hsmpcicard.service.name)
    db.session.delete(hsmpcicard)
    db.session.commit()
    flash(deleted_msg)

    return redirect(url_for('main.index'))
