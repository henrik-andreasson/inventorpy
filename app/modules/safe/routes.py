from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db, audit
from app.main import bp
from app.models import Location, User
from app.modules.hsm.models import HsmBackupUnit, HsmPed, HsmPin
from app.modules.safe.models import Safe, Compartment, PhysicalKey
from app.modules.safe.forms import SafeForm, CompartmentForm,\
 AuditCompartmentForm, PhysicalKeyForm
from flask_babel import _
from datetime import datetime
from sqlalchemy import desc, asc


@bp.route('/safe/add', methods=['GET', 'POST'])
@login_required
def safe_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = SafeForm(formdata=request.form)

    if request.method == 'POST' and form.validate_on_submit():

        location = Location.query.get(form.location.data)
        safe = Safe(name=form.name.data)
        safe.location = location
        db.session.add(safe)
        db.session.commit()
        audit.auditlog_new_post(
            'safe', original_data=safe.to_dict(), record_name=safe.name)

        flash(_('New Safe is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('safe.html', title=_('Safe'),
                               form=form)


@bp.route('/safe/edit/', methods=['GET', 'POST'])
@login_required
def safe_edit():

    safeid = request.args.get('safe')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.safe_delete', safe=safeid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.safe_qr', id=safeid))

    safe = Safe.query.get(safeid)
    form = SafeForm(obj=safe)

    if safe is None:
        flash(_('Safe not found'))
        return redirect(request.referrer)

    original_data = safe.to_dict()

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.get(form.location.data)

        safe.name = form.name.data
        safe.location = location
        db.session.commit()
        audit.auditlog_update_post(
            'safe', original_data=original_data, updated_data=safe.to_dict(), record_name=safe.name)

        flash(_('Your changes to the safe have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.location.data = safe.location_id

        return render_template('safe.html', title=_('Edit Safe'),
                               form=form)


@bp.route('/safe/list/', methods=['GET', 'POST'])
@login_required
def safe_list():

    page = request.args.get('page', 1, type=int)

    safes = Safe.query.order_by(Safe.name).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.safe_list', page=safes.next_num) \
        if safes.has_next else None
    prev_url = url_for('main.safe_list', page=safes.prev_num) \
        if safes.has_prev else None

    return render_template('safe.html', title=_('Safe'),
                           safes=safes.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/safe/content/', methods=['GET', 'POST'])
@login_required
def safe_content():

    safeid = request.args.get('safe')
    safe = Safe.query.get(safeid)
    if safe is None:
        flash(_('Safe not found'))
        return redirect(request.referrer)

    hsmbackupunits = HsmBackupUnit.query.filter_by(safe_id=safe.id)
    compartments = Compartment.query.filter_by(safe_id=safe.id)

    return render_template('safe.html', title=_('Safe'),
                           compartments=compartments,
                           hsmbackupunits=hsmbackupunits)


@bp.route('/safe/delete/', methods=['GET', 'POST'])
@login_required
def safe_delete():

    safeid = request.args.get('safe')
    safe = Safe.query.get(safeid)

    if safe is None:
        flash(_('Safe was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Safe deleted: %s %s' % (safe.name,
                                           safe.location.longName())
    db.session.delete(safe)
    db.session.commit()
    audit.auditlog_delete_post(
        'safe', data=safe.to_dict(), record_name=safe.name)
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/compartment/add', methods=['GET', 'POST'])
@login_required
def compartment_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = CompartmentForm(formdata=request.form)

    form.safe.choices = [(s.id, s.name) for s in Safe.query.all()]
    form.user.choices = [(u.id, u.username) for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(form.user.data)
        safe = Safe.query.get(form.safe.data)
        compartment = Compartment(name=form.name.data)
        compartment.safe = safe
        compartment.user = user
        db.session.add(compartment)
        db.session.commit()
        audit.auditlog_new_post(
            'compartment', original_data=compartment.to_dict(), record_name=compartment.name)

        flash(_('New Compartment is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('safe.html', title=_('Compartment'),
                               form=form)


@bp.route('/compartment/edit/', methods=['GET', 'POST'])
@login_required
def compartment_edit():

    compartmentid = request.args.get('compartment')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.compartment_delete', compartment=compartmentid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.compartment_qr', id=compartmentid))

    compartment = Compartment.query.get(compartmentid)
    original_data = compartment.to_dict()

    form = CompartmentForm(obj=compartment)

    if compartment is None:
        flash(_('Compartment not found'))
        return redirect(request.referrer)

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(form.user.data)
        safe = Safe.query.get(form.safe.data)
        compartment.name = form.name.data
        compartment.safe = safe
        compartment.user = user
        db.session.commit()
        audit.auditlog_update_post('compartment', original_data=original_data,
                                   updated_data=compartment.to_dict(), record_name=compartment.name)

        flash(_('Your changes to the compartment have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.user.data = compartment.user_id
        form.safe.data = compartment.safe_id
        if compartment.auditor_id is not None:
            auditor = User.query.get(compartment.auditor_id)
            form.auditor.data = auditor.username
        else:
            form.auditor.data = 'Not Audited'

        return render_template('safe.html', title=_('Edit Compartment'),
                               form=form)


@bp.route('/compartment/list/', methods=['GET', 'POST'])
@login_required
def compartment_list():

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'name')
    order = request.args.get('order', 'desc')

    sortstr = "{}(Compartment.{})".format(order, sort)
    compartments = Compartment.query.order_by(eval(sortstr)).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.compartment_list', page=compartments.next_num, sort=sort, order=order) \
        if compartments.has_next else None
    prev_url = url_for('main.compartment_list', page=compartments.prev_num, sort=sort, order=order) \
        if compartments.has_prev else None

    return render_template('safe.html', title=_('Compartment List'),
                           compartments=compartments.items, next_url=next_url,
                           prev_url=prev_url, order=order)


@bp.route('/compartment/delete/', methods=['GET', 'POST'])
@login_required
def compartment_delete():

    compartmentid = request.args.get('compartment')
    compartment = Compartment.query.get(compartmentid)

    if compartment is None:
        flash(_('Compartment was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Compartment deleted: %s' % (compartment.name)
    db.session.delete(compartment)
    db.session.commit()
    audit.auditlog_delete_post(
        'compartment', data=compartment.to_dict(), record_name=compartment.name)

    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/compartment/audit/', methods=['GET', 'POST'])
@login_required
def compartment_audit():

    compartmentid = request.args.get('compartment')

    compartment = Compartment.query.get(compartmentid)
    original_data = compartment.to_dict()

    form = AuditCompartmentForm(obj=compartment)

    if compartment is None:
        flash(_('Compartment not found'))
        return redirect(request.referrer)

    if request.method == 'POST' and form.validate_on_submit():
        auditor = User.query.filter_by(
            username=current_user.username).first_or_404()
        if current_user.username == compartment.user.username:
            flash(_('You are not allowed to audit your own compartment'))
            return redirect(request.referrer)

        if 'approved' in request.form:
            compartment.audit_status = "approved"
        elif 'failed' in request.form:
            compartment.audit_status = "failed"
        else:
            flash(_('Unknown auditor status'))
            return redirect(request.referrer)

        compartment.audit_date = datetime.utcnow()
        compartment.audit_comment = form.comment.data
        compartment.auditor_id = auditor.id
        db.session.commit()
        audit.auditlog_update_post('compartment', original_data=original_data,
                                   updated_data=compartment.to_dict(), record_name=compartment.name)

        flash(_('Your changes to the compartment have been saved.'))

        return redirect(url_for('main.compartment_list'))

    else:
        if current_user.username == compartment.user.username:
            flash(_('You are not allowed to audit your own compartment'))

        form.user.data = compartment.user.username
        form.safe.data = compartment.safe.name
        hsmpeds = HsmPed.query.filter_by(compartment_id=compartment.id)
        hsmpins = HsmPin.query.filter_by(compartment_id=compartment.id)

        return render_template('safe.html', title=_('Audit Compartment'),
                               hsmpeds=hsmpeds, hsmpins=hsmpins, form=form)


@bp.route('/safe/qr/<int:id>', methods=['GET'])
@login_required
def safe_qr(id):

    if id is None:
        flash(_('safe was not found, id not found!'))
        return redirect(url_for('main.index'))

    safe = None
    safe = Safe.query.get(id)

    if safe is None:
        flash(_('safe was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.safe_edit", safe=safe.id, _external=True)
    return render_template('safe_qr.html', title=_('QR Code'),
                           safe=safe, qr_data=qr_data)


@bp.route('/compartment/qr/<int:id>', methods=['GET'])
@login_required
def compartment_qr(id):

    if id is None:
        flash(_('compartment was not found, id not found!'))
        return redirect(url_for('main.index'))

    compartment = None
    compartment = Compartment.query.get(id)

    if compartment is None:
        flash(_('compartment was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.compartment_edit",
                      compartment=compartment.id, _external=True)
    return render_template('compartment_qr.html', title=_('QR Code'),
                           compartment=compartment, qr_data=qr_data)


@bp.route('/physicalkey/add', methods=['GET', 'POST'])
@login_required
def physicalkey_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = PhysicalKeyForm(formdata=request.form)

    if request.method == 'POST' and form.validate_on_submit():

        user = User.query.get(form.user.data)
        physicalkey = PhysicalKey(name=form.name.data)
        physicalkey.user = user
        db.session.add(physicalkey)
        db.session.commit()
        audit.auditlog_new_post(
            'physicalkey', original_data=physicalkey.to_dict(), record_name=physicalkey.name)

        flash(_('New PhysicalKey is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('physicalkey.html', title=_('PhysicalKey'),
                               form=form)


@bp.route('/physicalkey/edit/', methods=['GET', 'POST'])
@login_required
def physicalkey_edit():

    physicalkeyid = request.args.get('physicalkey')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.physicalkey_delete', physicalkey=physicalkeyid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.physicalkey_qr', id=physicalkeyid))

    physicalkey = PhysicalKey.query.get(physicalkeyid)
    form = PhysicalKeyForm(obj=physicalkey)

    if physicalkey is None:
        flash(_('PhysicalKey not found'))
        return redirect(request.referrer)

    original_data = physicalkey.to_dict()

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.get(form.location.data)

        physicalkey.name = form.name.data
        physicalkey.location = location
        db.session.commit()
        audit.auditlog_update_post('physicalkey', original_data=original_data,
                                   updated_data=physicalkey.to_dict(), record_name=physicalkey.name)

        flash(_('Your changes to the physicalkey have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.location.data = physicalkey.location_id

        return render_template('physicalkey.html', title=_('Edit PhysicalKey'),
                               form=form)


@bp.route('/physicalkey/list/', methods=['GET', 'POST'])
@login_required
def physicalkey_list():

    page = request.args.get('page', 1, type=int)

    physicalkeys = PhysicalKey.query.order_by(PhysicalKey.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.physicalkey_list', page=physicalkeys.next_num) \
        if physicalkeys.has_next else None
    prev_url = url_for('main.physicalkey_list', page=physicalkeys.prev_num) \
        if physicalkeys.has_prev else None

    return render_template('physicalkey.html', title=_('PhysicalKey'),
                           physicalkeys=physicalkeys.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/physicalkey/content/', methods=['GET', 'POST'])
@login_required
def physicalkey_content():

    physicalkeyid = request.args.get('physicalkey')
    physicalkey = PhysicalKey.query.get(physicalkeyid)
    if physicalkey is None:
        flash(_('PhysicalKey not found'))
        return redirect(request.referrer)

    hsmbackupunits = HsmBackupUnit.query.filter_by(
        physicalkey_id=physicalkey.id)
    compartments = Compartment.query.filter_by(physicalkey_id=physicalkey.id)

    return render_template('physicalkey.html', title=_('PhysicalKey'),
                           compartments=compartments,
                           hsmbackupunits=hsmbackupunits)


@bp.route('/physicalkey/delete/', methods=['GET', 'POST'])
@login_required
def physicalkey_delete():

    physicalkeyid = request.args.get('physicalkey')
    physicalkey = PhysicalKey.query.get(physicalkeyid)

    if physicalkey is None:
        flash(_('PhysicalKey was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'PhysicalKey deleted: %s %s' % (physicalkey.name,
                                                  physicalkey.location.longName())
    db.session.delete(physicalkey)
    db.session.commit()
    audit.auditlog_delete_post(
        'physicalkey', data=physicalkey.to_dict(), record_name=physicalkey.name)
    flash(deleted_msg)

    return redirect(url_for('main.index'))
