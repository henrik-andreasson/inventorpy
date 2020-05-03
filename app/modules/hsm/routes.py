from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import login_required, current_user
from app import db, audit
from app.main import bp
from app.models import Service, User
from app.modules.server.models import Server
from app.modules.safe.models import Compartment, Safe
from app.modules.hsm.models import HsmDomain, HsmPed, HsmPin, HsmBackupUnit, \
    HsmPciCard, HsmPedUpdates
from app.modules.hsm.forms import HsmDomainForm, HsmPedForm, HsmPinForm, \
    HsmPciCardForm, HsmBackupUnitForm, HsmPedUpdateForm
from flask_babel import _


@bp.route('/hsm/domain/add', methods=['GET', 'POST'])
@login_required
def hsm_domain_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmDomainForm(formdata=request.form)
    #
    # if 'selected_service' in session:
    #     service = Service.query.filter_by(name=session['selected_service']).first()
    #     form.service.choices = [(service.name, service.name)]
    #
    # else:
    #     form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(id=form.service.data).first()

        hsmdomain = HsmDomain(name=form.name.data)
        hsmdomain.service_id = service.id
        db.session.add(hsmdomain)
        db.session.commit()
        audit.auditlog_new_post('hsm_domain', original_data=hsmdomain.to_dict(), record_name=hsmdomain.name)

        flash(_('New HSM Domain is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('HSM'),
                               form=form)


@bp.route('/hsm/domain/edit/', methods=['GET', 'POST'])
@login_required
def hsm_domain_edit():

    domainid = request.args.get('domain')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_domain_delete', domain=domainid))

    hsmdomain = HsmDomain.query.get(domainid)
    original_data = hsmdomain.to_dict()

    form = HsmDomainForm(obj=hsmdomain)

    # if 'selected_service' in session:
    #     service = Service.query.filter_by(name=session['selected_service']).first()
    #     form.service.choices = [(service.name, service.name)]
    #
    # else:
    #     form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    if hsmdomain is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(id=form.service.data).first()
        hsmdomain.name = form.name.data
        hsmdomain.service_id = service.id

        db.session.commit()
        audit.auditlog_update_post('hsm_domain', original_data=original_data, updated_data=hsmdomain.to_dict(), record_name=hsmdomain.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.service.data = hsmdomain.service_id
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
    audit.auditlog_delete_post('hsm_domain', data=hsmdomain.to_dict())
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/ped/add', methods=['GET', 'POST'])
@login_required
def hsm_ped_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPedForm()

    # form.compartment.choices = [(c.id, '{} ({})'.format(c.name, c.user.username)) for c in Compartment.query.all()]
    # form.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.all()]
    # form.user.choices = [(u.id, u.username) for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        hsmped = HsmPed(keyno=form.keyno.data,
                        keysn=form.keysn.data)
        hsmped.compartment = Compartment.query.filter_by(id=form.compartment.data).first_or_404()
        hsmped.hsmdomain = HsmDomain.query.filter_by(id=form.hsmdomain.data).first_or_404()
        hsmped.user = User.query.filter_by(id=form.user.data).first_or_404()
        db.session.add(hsmped)
        db.session.commit()
        audit.auditlog_new_post('hsm_ped', original_data=hsmped.to_dict(), record_name=hsmped.keyno)

        flash(_('New HSM PED is now posted!'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('HSM'),
                               form=form)


@bp.route('/hsm/ped/edit/', methods=['GET', 'POST'])
@login_required
def hsm_ped_edit():

    pedid = request.args.get('ped')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_ped_delete', ped=pedid))

    hsmped = HsmPed.query.get(pedid)
    original_data = hsmped.to_dict()

    if hsmped is None:
        render_template('hsm.html', title=_('HSM PED is not defined'))

    form = HsmPedForm(obj=hsmped)

    if request.method == 'POST' and form.validate_on_submit():

        hsmpedupdate = HsmPedUpdates(keyno=form.keyno.data,
                                     keysn=form.keysn.data)
        hsmpedupdate.compartment = Compartment.query.filter_by(id=form.compartment.data).first_or_404()
        hsmpedupdate.hsmdomain = HsmDomain.query.filter_by(id=form.hsmdomain.data).first_or_404()
        hsmpedupdate.user = User.query.filter_by(id=form.user.data).first_or_404()
        db.session.add(hsmpedupdate)
        db.session.commit()

        audit.auditlog_update_post('hsm_ped', original_data=original_data, updated_data=hsmped.to_dict(), record_name=hsmped.keyno)

        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.compartment.data = hsmped.compartment_id
        form.hsmdomain.data = hsmped.hsmdomain_id
        form.user.data = hsmped.user_id
        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/ped/approve/', methods=['GET', 'POST'])
@login_required
def hsm_ped_approve():

    pedid = request.args.get('ped')

    hsmpedupdate = HsmPedUpdates.query.get(pedid)
    original_data = hsmpedupdate.to_dict()

    if hsmpedupdate is None:
        render_template('hsm.html', title=_('HSM PED Update is not defined'))

    if 'postpone' in request.form:
        return redirect(request.referrer)
    if 'deny' in request.form:
        db.session.delete(hsmpedupdate)
        db.session.commit()
        flash("Pending Approval was denied")
        return redirect(url_for('main.index'))

    form = HsmPedUpdateForm(obj=hsmpedupdate)

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(name=hsmpedupdate.hsmdomain.service.name).first()
        if current_user.username != service.manager.username:
            flash(_('You are not the service manager of the service thus not allowed to approve this action'))
            return redirect(request.referrer)

        hsmped = HsmPed.query.get(pedid)
        hsmped.keyno = form.keyno.data
        hsmped.keysn = form.keysn.data
        hsmped.compartment = Compartment.query.filter_by(id=form.compartment.data).first_or_404()
        hsmped.hsmdomain = HsmDomain.query.filter_by(id=form.hsmdomain.data).first_or_404()
        hsmped.user = User.query.filter_by(id=form.user.data).first_or_404()
        db.session.delete(hsmpedupdate)
        db.session.commit()

        audit.auditlog_update_post('hsm_ped', original_data=original_data, updated_data=hsmped.to_dict(), record_name=hsmped.keyno)

        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        service = Service.query.filter_by(name=hsmpedupdate.hsmdomain.service.name).first()
        flash(_('Only the service manager ({}) of the service are allowed to approve this action'.format(service.manager.username)))

        form.compartment.data = hsmpedupdate.compartment_id
        form.hsmdomain.data = hsmpedupdate.hsmdomain_id
        form.user.data = hsmpedupdate.user_id
        previous_ped = HsmPed.query.get(pedid)
        hsmpeds = []
        hsmpeds.append(previous_ped)
        if previous_ped is None:
            render_template('hsm.html', title=_('HSM PED Update is not defined'))

        return render_template('hsm.html', title=_('Approve HSM PED Update'),
                               form=form, hsmpeds=hsmpeds)


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
    audit.auditlog_delete_post('hsm_ped', data=hsmped.to_dict(), record_name=hsmped.keyno)
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pin/add', methods=['GET', 'POST'])
@login_required
def hsm_pin_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPinForm()
    # form.ped.choices = [(p.id, '{}-{} ({})'.format(p.keyno, p.keysn, p.user.username)) for p in HsmPed.query.all()]
    # form.compartment.choices = [(c.id, '{} - {}'.format(c.name, c.user.username)) for c in Compartment.query.all()]
    # form.compartment.choices.insert(0, (0, 'None'))

    if request.method == 'POST' and form.validate_on_submit():
        hsmpin = HsmPin()
        hsmpin.ped = HsmPed.query.get(form.ped.data)
        hsmpin.compartment = Compartment.query.get(form.compartment.data)
        db.session.add(hsmpin)
        db.session.commit()
        audit.auditlog_new_post('hsm_pin', original_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

        flash(_('New HSM PIN is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('HSM PIN'),
                               form=form)


@bp.route('/hsm/pin/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pin_edit():

    pinid = request.args.get('pin')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pin_delete', pin=pinid))

    hsmpin = HsmPin.query.get(pinid)
    original_data = hsmpin.to_dict()

    form = HsmPinForm(obj=hsmpin)

    if hsmpin is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        hsmpin.compartment_id = form.compartment.data
        hsmpin.ped_id = form.ped.data

        db.session.commit()
        audit.auditlog_update_post('hsm_pin', original_data=original_data, updated_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.ped.data = hsmpin.ped_id
        form.compartment.data = hsmpin.compartment_id
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
    audit.auditlog_delete_post('hsm_ped', data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pcicard/add', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPciCardForm()

    if request.method == 'POST' and form.validate_on_submit():

        if form.server.data == 0 and form.compartment.data == 0:
            flash(_('Must select server OR compartment!'))
            return redirect(request.referrer)

        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        server = Server.query.get(form.server.data)
        compartment = Compartment.query.get(form.compartment.data)
        hsmpcicard = HsmPciCard(serial=form.serial.data,
                                model=form.model.data,
                                manufacturedate=form.manufacturedate.data,
                                fbno=form.fbno.data)
        hsmpcicard.hsmdomain = hsmdomain
        hsmpcicard.compartment = compartment
        hsmpcicard.server = server
        db.session.add(hsmpcicard)
        db.session.commit()
        audit.auditlog_new_post('hsm_pci_card', original_data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)

        flash(_('New HSM PCI is now posted!'))

        return redirect(url_for('main.index'))

    else:

#        hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.id.desc()).limit(10)
        return render_template('hsm.html', title=_('HSM'),
                               form=form)


@bp.route('/hsm/pcicard/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_edit():

    pcicardid = request.args.get('pcicard')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pcicard_delete', pcicard=pcicardid))

    hsmpcicard = HsmPciCard.query.get(pcicardid)
    original_data = hsmpcicard.to_dict()

    form = HsmPciCardForm(obj=hsmpcicard)
    # form.hsmdomain.choices = [(h.id, h.name) for h in HsmDomain.query.all()]
    # form.server.choices = [(s.id, s.hostname) for s in Server.query.all()]
    # form.compartment.choices = [(c.id, c.name) for c in Compartment.query.all()]

    if hsmpcicard is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        server = Server.query.get(form.server.data)
        compartment = Compartment.query.get(form.compartment.data)
        hsmpcicard.fbno = form.fbno.data
        hsmpcicard.serial = form.serial.data
        hsmpcicard.model = form.model.data
        hsmpcicard.manufacturedate = form.manufacturedate.data
        hsmpcicard.hsmdomain = hsmdomain
        hsmpcicard.compartment = compartment
        hsmpcicard.server = server

        db.session.commit()
        audit.auditlog_update_post('hsm_pci_card', original_data=original_data, updated_data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:

        form.hsmdomain.data = hsmpcicard.hsmdomain_id
        form.compartment.data = hsmpcicard.compartment_id
        form.server.data = hsmpcicard.server_id

        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/pcicard/list/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_list():

    page = request.args.get('page', 1, type=int)

    hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.id).paginate(
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
    audit.auditlog_delete_post('hsm_ped', data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)

    return redirect(url_for('main.index'))


@bp.route('/hsm/backupunit/add', methods=['GET', 'POST'])
@login_required
def hsm_backupunit_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmBackupUnitForm()

    if request.method == 'POST' and form.validate_on_submit():

        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        safe = Safe.query.get(form.safe.data)
        hsmbackupunit = HsmBackupUnit(name=form.name.data,
                                      serial=form.serial.data,
                                      model=form.model.data,
                                      manufacturedate=form.manufacturedate.data,
                                      fbno=form.fbno.data,
                                      comment=form.comment.data)
        hsmbackupunit.hsmdomain = hsmdomain
        hsmbackupunit.safe = safe
        db.session.add(hsmbackupunit)
        db.session.commit()
        audit.auditlog_new_post('hsm_backup_unit', original_data=hsmbackupunit.to_dict(), record_name=hsmbackupunit.serial)

        flash(_('Added HSM backupunit {} - {}'.format(hsmbackupunit.name, hsmbackupunit.serial)))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('HSM'),
                               form=form)


@bp.route('/hsm/backupunit/edit/', methods=['GET', 'POST'])
@login_required
def hsm_backupunit_edit():

    backupunitid = request.args.get('id')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_backupunit_delete', backupunit=backupunitid))

    hsmbackupunit = HsmBackupUnit.query.get(backupunitid)

    if hsmbackupunit is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    original_data = hsmbackupunit.to_dict()

    form = HsmBackupUnitForm(obj=hsmbackupunit)

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        safe = Safe.query.get(form.safe.data)
        hsmbackupunit.name = form.name.data
        hsmbackupunit.serial = form.serial.data
        hsmbackupunit.model = form.model.data
        hsmbackupunit.manufacturedate = form.manufacturedate.data
        hsmbackupunit.fbno = form.fbno.data
        hsmbackupunit.hsmdomain = hsmdomain
        hsmbackupunit.safe = safe
        hsmbackupunit.comment = form.comment.data

        db.session.commit()
        audit.auditlog_update_post('hsm_backup_unit', original_data=original_data, updated_data=hsmbackupunit.to_dict(), record_name=hsmbackupunit.serial)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:

        form.hsmdomain.data = hsmbackupunit.hsmdomain_id
        form.safe.data = hsmbackupunit.safe_id

        return render_template('hsm.html', title=_('Edit HSM Domain'),
                               form=form)


@bp.route('/hsm/backupunit/list/', methods=['GET', 'POST'])
@login_required
def hsm_backupunit_list():

    page = request.args.get('page', 1, type=int)

    hsmbackupunits = HsmBackupUnit.query.order_by(HsmBackupUnit.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.hsm_domain_list', page=hsmbackupunits.next_num) \
        if hsmbackupunits.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmbackupunits.prev_num) \
        if hsmbackupunits.has_prev else None

    return render_template('hsm.html', title=_('HSM Domains'),
                           hsmbackupunits=hsmbackupunits.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/hsm/backupunit/delete/', methods=['GET', 'POST'])
@login_required
def hsm_backupunit_delete():

    backupunitid = request.args.get('backupunit')
    hsmbackupunit = HsmBackupUnit.query.get(backupunitid)

    if hsmbackupunit is None:
        flash(_('HSM PED was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'HSM PED deleted: %s %s' % (hsmbackupunit.keyno,
                                              hsmbackupunit.service.name)
    db.session.delete(hsmbackupunit)
    db.session.commit()
    flash(deleted_msg)
    audit.auditlog_delete_post('hsm_ped', data=hsmbackupunit.to_dict(), record_name=hsmbackupunit.serial)

    return redirect(url_for('main.index'))
