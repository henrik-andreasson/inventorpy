from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import login_required, current_user
from app import db, audit
from app.main import bp
from app.models import Service, User
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

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(id=form.service.data).first()

        hsmdomain = HsmDomain(name=form.name.data)
        hsmdomain.service_id = service.id
        db.session.add(hsmdomain)
        db.session.commit()
        audit.auditlog_new_post(
            'hsm_domain', original_data=hsmdomain.to_dict(), record_name=hsmdomain.name)

        flash(_('New HSM Domain is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('Add HSM Domain'),
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

    if hsmdomain is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(id=form.service.data).first()
        hsmdomain.name = form.name.data
        hsmdomain.service_id = service.id

        db.session.commit()
        audit.auditlog_update_post('hsm_domain', original_data=original_data,
                                   updated_data=hsmdomain.to_dict(), record_name=hsmdomain.name)
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
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.hsm_domain_list', page=hsmdomains.next_num) \
        if hsmdomains.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmdomains.prev_num) \
        if hsmdomains.has_prev else None

    return render_template('hsm.html', title=_('List HSM Domains'),
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

    if request.method == 'POST' and form.validate_on_submit():
        hsmped = HsmPed(keyno=form.keyno.data,
                        keysn=form.keysn.data,
                        type=form.type.data,
                        comment=form.comment.data)
        hsmped.compartment = Compartment.query.filter_by(
            id=form.compartment.data).first_or_404()
        hsmped.hsmdomain = HsmDomain.query.filter_by(
            id=form.hsmdomain.data).first_or_404()
        hsmped.user = User.query.filter_by(id=form.user.data).first_or_404()
        db.session.add(hsmped)
        db.session.commit()
        audit.auditlog_new_post(
            'hsm_ped', original_data=hsmped.to_dict(), record_name=hsmped.keyno)

        flash(_('New HSM PED is now posted!'))

        return redirect(url_for('main.index'))

    else:
        return render_template('hsm.html', title=_('Add HSM Ped'),
                               form=form)


@bp.route('/hsm/ped/edit/', methods=['GET', 'POST'])
@login_required
def hsm_ped_edit():

    pedid = request.args.get('ped')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_ped_delete', ped=pedid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.hsm_ped_qr', id=pedid))

    hsmped = HsmPed.query.get(pedid)
    if hsmped is None:
        flash(_(f'No ped is found with id {pedid}.'))
        return redirect(url_for('main.index'))

    original_data = hsmped.to_dict()

    form = HsmPedForm(obj=hsmped)

    if request.method == 'POST' and form.validate_on_submit():

        if current_app.config['PED_HANDOVER_MUST_BE_APPROVED'] is True:

            hsmpedupdate = HsmPedUpdates(keyno=form.keyno.data,
                                         keysn=form.keysn.data,
                                         type=form.type.data)
            hsmpedupdate.ped = HsmPed.query.filter_by(
                id=form.hsmped.data).first_or_404()
            hsmpedupdate.compartment = Compartment.query.filter_by(
                id=form.compartment.data).first_or_404()
            hsmpedupdate.hsmdomain = HsmDomain.query.filter_by(
                id=form.hsmdomain.data).first_or_404()
            hsmpedupdate.user = User.query.filter_by(
                id=form.user.data).first_or_404()
            db.session.add(hsmpedupdate)
            db.session.commit()

            audit.auditlog_update_post('hsm_ped', original_data=original_data,
                                       updated_data=hsmped.to_dict(), record_name=hsmped.keyno)

            flash(_('Your changes must be approved.'))
        else:
            # TODO: creates a new PED !!!!
            hsmped = HsmPed(keyno=form.keyno.data,
                            keysn=form.keysn.data,
                            type=form.type.data)
            hsmped.compartment = Compartment.query.filter_by(
                            id=form.compartment.data).first_or_404()
            hsmped.hsmdomain = HsmDomain.query.filter_by(
                            id=form.hsmdomain.data).first_or_404()
            hsmped.user = User.query.filter_by(
                            id=form.user.data).first_or_404()
            db.session.add(hsmped)
            db.session.commit()
            flash(_('Your changes has been committed.'))

        return redirect(url_for('main.index'))

    else:
        form.compartment.data = hsmped.compartment_id
        form.hsmdomain.data = hsmped.hsmdomain_id
        form.user.data = hsmped.user_id
        form.hsmped.data = hsmped.id

        return render_template('hsm.html', title=_('Edit HSM Ped'),
                               form=form)


@bp.route('/hsm/ped/approve/', methods=['GET', 'POST'])
@login_required
def hsm_ped_approve():

    pedid = request.args.get('ped')


    if 'postpone' in request.form:
        return redirect(request.referrer)
    if 'deny' in request.form:
        db.session.delete(hsmpedupdate)
        db.session.commit()
        flash("Pending Approval was denied")
        return redirect(url_for('main.index'))


    hsmpedupdate = HsmPedUpdates.query.get(pedid)
    if hsmpedupdate is None:
        flash(_(f'Ped not found {pedid}.'))
        return redirect(url_for('main.index'))

    org_hsmped = HsmPed.query.get(hsmpedupdate.ped_id)
    original_data = org_hsmped.to_dict()
    form = HsmPedUpdateForm(obj=hsmpedupdate.ped_id)

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(
            name=hsmpedupdate.hsmdomain.service.name).first()
        if current_user.username != service.manager.username:
            flash(
                _(f'You({current_user.username}) are not the service manager({service.manager.username}) of the service thus not allowed to approve this action'))
            return redirect(request.referrer)

        upd_hsmped = HsmPed.query.get(form.hsmped.data)
        if upd_hsmped is None:
            flash(_('hsm PED not found.'))
            return redirect(url_for('main.index'))

        upd_hsmped.keyno = form.keyno.data
        upd_hsmped.keysn = form.keysn.data
        upd_hsmped.compartment = Compartment.query.filter_by(
            id=form.compartment.data).first_or_404()
        upd_hsmped.hsmdomain = HsmDomain.query.filter_by(
            id=form.hsmdomain.data).first_or_404()
        upd_hsmped.user = User.query.filter_by(id=form.user.data).first_or_404()
        db.session.delete(hsmpedupdate)
        db.session.commit()

        audit.auditlog_update_post('hsm_ped', original_data=original_data,
                                   updated_data=upd_hsmped.to_dict(), record_name=upd_hsmped.keysn)

        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:


        service = Service.query.filter_by(
            name=hsmpedupdate.hsmdomain.service.name).first()
        form.compartment.data = hsmpedupdate.compartment_id
        form.hsmdomain.data = hsmpedupdate.hsmdomain_id
        form.type.data = hsmpedupdate.type
        form.keysn.data = hsmpedupdate.keysn
        form.keyno.data = hsmpedupdate.keyno
        form.user.data = hsmpedupdate.user_id
        form.hsmped.data = hsmpedupdate.ped_id
        form.comment.data = hsmpedupdate.comment

        ped_org_data = []
        ped_org_data.append(org_hsmped)

        return render_template('hsm.html', title=_('Approve HSM PED Update'),
                               hsmpedupdate=hsmpedupdate,
                               form=form,
                               ped_org_data=ped_org_data)


@bp.route('/hsm/ped/list/', methods=['GET', 'POST'])
@login_required
def hsm_ped_list():

    page = request.args.get('page', 1, type=int)

    hsmpeds = HsmPed.query.order_by(HsmPed.keysn).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.hsm_ped_list', page=hsmpeds.next_num) \
        if hsmpeds.has_next else None
    prev_url = url_for('main.hsm_ped_list', page=hsmpeds.prev_num) \
        if hsmpeds.has_prev else None

    return render_template('hsm.html', title=_('List HSM Peds'),
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
    audit.auditlog_delete_post(
        'hsm_ped', data=hsmped.to_dict(), record_name=hsmped.keyno)
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pin/add', methods=['GET', 'POST'])
@login_required
def hsm_pin_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPinForm()

    if request.method == 'POST' and form.validate_on_submit():
        hsmpin = HsmPin()
        hsmpin.ped = HsmPed.query.get(form.ped.data)
        hsmpin.compartment = Compartment.query.get(form.compartment.data)
        db.session.add(hsmpin)
        db.session.commit()
        audit.auditlog_new_post(
            'hsm_pin', original_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

        flash(_('New HSM PIN is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('Add HSM PIN'),
                               form=form)


@bp.route('/hsm/pin/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pin_edit():

    pinid = request.args.get('pin')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pin_delete', pin=pinid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.hsm_pin_qr', id=pinid))

    hsmpin = HsmPin.query.get(pinid)
    original_data = hsmpin.to_dict()

    form = HsmPinForm(obj=hsmpin)
    # for field in form:
    #     if field.flags.required:
    #         form.field.label = Label(text=field.label.text + ' *')

    if hsmpin is None:
        render_template('hsm.html', title=_('HSM Domain is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        hsmpin.compartment_id = form.compartment.data
        hsmpin.ped_id = form.ped.data

        db.session.commit()
        audit.auditlog_update_post('hsm_pin', original_data=original_data,
                                   updated_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.ped.data = hsmpin.ped_id
        form.compartment.data = hsmpin.compartment_id
        return render_template('hsm.html', title=_('Edit HSM PIN'),
                               form=form)


@bp.route('/hsm/pin/list/', methods=['GET', 'POST'])
@login_required
def hsm_pin_list():

    page = request.args.get('page', 1, type=int)

    hsmpins = HsmPin.query.order_by(HsmPin.id).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.hsm_pin_list', page=hsmpins.next_num) \
        if hsmpins.has_next else None
    prev_url = url_for('main.hsm_pin_list', page=hsmpins.prev_num) \
        if hsmpins.has_prev else None

    return render_template('hsm.html', title=_('List HSM PINs'),
                           hsmpins=hsmpins, next_url=next_url,
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
    audit.auditlog_delete_post(
        'hsm_ped', data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pcicard/add', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_add():
    from app.modules.server.models import Server

    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = HsmPciCardForm()

    if request.method == 'POST' and form.validate_on_submit():

        if form.server.data == 0 and form.compartment.data == 0:
            flash(_('Must select server OR compartment!'))
            return redirect(request.referrer)

        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        server = Server.query.get(form.server.data)
        safe = Safe.query.get(form.safe.data)
        hsmpcicard = HsmPciCard(serial=form.serial.data,
                                model=form.model.data,
                                manufacturedate=form.manufacturedate.data,
                                fbno=form.fbno.data)
        hsmpcicard.hsmdomain = hsmdomain
        hsmpcicard.safe = safe
        hsmpcicard.server = server
        db.session.add(hsmpcicard)
        db.session.commit()
        audit.auditlog_new_post(
            'hsm_pci_card', original_data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)

        flash(_('New HSM PCI is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('Add HSM PCI Card '),
                               form=form)


@bp.route('/hsm/pcicard/edit/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_edit():

    from app.modules.server.models import Server

    pcicardid = request.args.get('pcicard')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_pcicard_delete', pcicard=pcicardid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.hsm_pcicard_qr', id=pcicardid))

    hsmpcicard = HsmPciCard.query.get(pcicardid)
    original_data = hsmpcicard.to_dict()

    form = HsmPciCardForm(obj=hsmpcicard)

    if hsmpcicard is None:
        render_template('hsm.html', title=_('HSM PCI Card is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        hsmdomain = HsmDomain.query.get(form.hsmdomain.data)
        server = Server.query.get(form.server.data)
        safe = Safe.query.get(form.safe.data)
        hsmpcicard.fbno = form.fbno.data
        hsmpcicard.serial = form.serial.data
        hsmpcicard.model = form.model.data
        hsmpcicard.manufacturedate = form.manufacturedate.data
        hsmpcicard.hsmdomain = hsmdomain
        hsmpcicard.safe = safe
        hsmpcicard.server = server

        db.session.commit()
        audit.auditlog_update_post('hsm_pci_card', original_data=original_data,
                                   updated_data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:

        form.hsmdomain.data = hsmpcicard.hsmdomain_id
        form.safe.data = hsmpcicard.safe_id
        form.server.data = hsmpcicard.server_id

        return render_template('hsm.html', title=_('Edit HSM PCI Card'),
                               form=form)


@bp.route('/hsm/pcicard/list/', methods=['GET', 'POST'])
@login_required
def hsm_pcicard_list():

    page = request.args.get('page', 1, type=int)
    serverid = request.args.get('serverid')

    if serverid is not None:
        hsmpcicards = HsmPciCard.query.filter_by(server_id=serverid).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    else:
        hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.id).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.hsm_domain_list', page=hsmpcicards.next_num) \
        if hsmpcicards.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmpcicards.prev_num) \
        if hsmpcicards.has_prev else None

    return render_template('hsm.html', title=_('List HSM PCI Cards'),
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

    deleted_msg = f'HSM PED deleted: {hsmpcicard.serial} {hsmpcicard.name}\
                    {hsmpcicard.hsmdomain.service.name}'
    db.session.delete(hsmpcicard)
    db.session.commit()
    flash(deleted_msg)
    audit.auditlog_delete_post(
        'hsm_ped', data=hsmpcicard.to_dict(), record_name=hsmpcicard.serial)

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
        audit.auditlog_new_post('hsm_backup_unit', original_data=hsmbackupunit.to_dict(
        ), record_name=hsmbackupunit.serial)

        flash(_('Added HSM backupunit {} - {}'.format(hsmbackupunit.name, hsmbackupunit.serial)))

        return redirect(url_for('main.index'))

    else:

        return render_template('hsm.html', title=_('Add HSM Backupunit'),
                               form=form)


@bp.route('/hsm/backupunit/edit/', methods=['GET', 'POST'])
@login_required
def hsm_backupunit_edit():

    backupunitid = request.args.get('id')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.hsm_backupunit_delete', backupunit=backupunitid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.hsm_backupunit_qr', id=backupunitid))

    hsmbackupunit = HsmBackupUnit.query.get(backupunitid)

    if hsmbackupunit is None:
        render_template('hsm.html', title=_('HSM Backupunit is not defined'))

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
        audit.auditlog_update_post('hsm_backup_unit', original_data=original_data,
                                   updated_data=hsmbackupunit.to_dict(), record_name=hsmbackupunit.serial)
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
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.hsm_domain_list', page=hsmbackupunits.next_num) \
        if hsmbackupunits.has_next else None
    prev_url = url_for('main.hsm_domain_list', page=hsmbackupunits.prev_num) \
        if hsmbackupunits.has_prev else None

    return render_template('hsm.html', title=_('List HSM Backup unit'),
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

    deleted_msg = 'HSM PED deleted: %s %s' % (hsmbackupunit.serial,
                                              hsmbackupunit.name)
    db.session.delete(hsmbackupunit)
    db.session.commit()
    flash(deleted_msg)
    audit.auditlog_delete_post(
        'hsm_ped', data=hsmbackupunit.to_dict(), record_name=hsmbackupunit.serial)

    return redirect(url_for('main.index'))


@bp.route('/hsm/pcicard/qr/<int:id>', methods=['GET'])
@login_required
def hsm_pcicard_qr(id):

    if id is None:
        flash(_('pcicard was not found, id not found!'))
        return redirect(url_for('main.index'))

    hsmpcicard = None
    hsmpcicard = HsmPciCard.query.get(id)

    if hsmpcicard is None:
        flash(_('hsmpcicard was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.hsm_pcicard_edit",
                      hsmpcicard=hsmpcicard.id, _external=True)

    return render_template('hsm_qr.html', title=_('QR Code'),
                           hsmpcicard=hsmpcicard, qr_data=qr_data)


@bp.route('/hsm/backupunit/qr/<int:id>', methods=['GET'])
@login_required
def hsm_backupunit_qr(id):

    if id is None:
        flash(_('backupunit was not found, id not found!'))
        return redirect(url_for('main.index'))

    hsmbackupunit = None
    hsmbackupunit = HsmBackupUnit.query.get(id)

    if hsmbackupunit is None:
        flash(_('backupunit was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.hsm_backupunit_edit",
                      id=hsmbackupunit.id, _external=True)

    return render_template('hsm_qr.html', title=_('QR Code'),
                           hsmbackupunit=hsmbackupunit, qr_data=qr_data)


@bp.route('/hsm/ped/qr/<int:id>', methods=['GET'])
@login_required
def hsm_ped_qr(id):

    if id is None:
        flash(_('ped was not found, id not found!'))
        return redirect(url_for('main.index'))

    hsmped = HsmPed.query.get(id)
    if hsmped is None:
        flash(_('hsmped was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.hsm_ped_edit", hsmped=hsmped.id, _external=True)

    return render_template('hsm_qr.html', title=_('QR Code'),
                           hsmped=hsmped, qr_data=qr_data)


@bp.route('/hsm/pin/qr/<int:id>', methods=['GET'])
@login_required
def hsm_pin_qr(id):

    if id is None:
        flash(_('pin was not found, id not found!'))
        return redirect(url_for('main.index'))

    hsmpin = HsmPin.query.get(id)
    if hsmpin is None:
        flash(_('hsmpin was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.hsm_pin_edit", hsmpin=hsmpin.id, _external=True)

    return render_template('hsm_qr.html', title=_('QR Code'),
                           hsmpin=hsmpin, qr_data=qr_data)
