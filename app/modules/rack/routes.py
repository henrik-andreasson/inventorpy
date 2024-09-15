from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app import db, audit
from app.main import bp
from app.models import Location
from app.modules.rack.models import Rack
from app.modules.rack.forms import RackForm, AuditRackForm
from flask_babel import _
from app.modules.switch.models import Switch
from app.modules.firewall.models import Firewall
from app.models import User
from datetime import datetime


@bp.route('/rack/add', methods=['GET', 'POST'])
@login_required
def rack_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = RackForm(formdata=request.form)

    location_choices = []
    for l in Location.query.all():
        newloc = (l.id, l.longName())
        location_choices.append(newloc)
    form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():

        location = Location.query.get(form.location.data)
        rack = Rack(name=form.name.data)
        rack.location = location
        db.session.add(rack)
        db.session.commit()
        audit.auditlog_new_post('rack', original_data=rack.to_dict(), record_name=rack.name)

        flash(_('New Rack is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('rack.html', title=_('Rack'),
                               form=form)


@bp.route('/rack/edit/', methods=['GET', 'POST'])
@login_required
def rack_edit():

    rackid = request.args.get('rack')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.rack_delete', rack=rackid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.rack_qr', id=rackid))

    rack = Rack.query.get(rackid)
    if rack is None:
        flash(_('Rack not found'))
        return redirect(request.referrer)

    form = RackForm(formdata=request.form, obj=rack)
    original_data = rack.to_dict()

    if request.method == 'POST' and form.validate_on_submit():

        rack.name = form.name.data
        rack.location_id = form.location.data

        db.session.commit()
        audit.auditlog_update_post('rack', original_data=original_data, updated_data=rack.to_dict(), record_name=rack.name)
        flash(_('Your changes to the rack have been saved.'))

        return redirect(url_for('main.index'))

    else:
        if rack.location is not None:
            form.location.data = rack.location.id
        return render_template('rack.html', title=_('Edit Rack'),
                               form=form)


@bp.route('/rack/list/', methods=['GET', 'POST'])
@login_required
def rack_list():

    page = request.args.get('page', 1, type=int)

    racks = Rack.query.order_by(Rack.name).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.rack_list', page=racks.next_num) \
        if racks.has_next else None
    prev_url = url_for('main.rack_list', page=racks.prev_num) \
        if racks.has_prev else None

    return render_template('rack.html', title=_('Rack'),
                           racks=racks.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/rack/content/', methods=['GET', 'POST'])
@login_required
def rack_content():

    rack_id = request.args.get('rack')
    rack = Rack.query.get(rack_id)
    if rack is None:
        flash(_('Rack not found'))
        return redirect(request.referrer)

    from app.modules.server.models import Server

    servers = Server.query.filter_by(rack_id=rack.id)
    switchs = Switch.query.filter_by(rack_id=rack.id)
    fws = Firewall.query.filter(Firewall.rack_id == rack.id)

    return render_template('rack.html', title=_('Rack contents'),
                           server_title=_('Servers'),
                           firewall_title=_('Firewalls'),
                           switch_title=_('Switches'),
                           servers=servers, switchs=switchs,
                           firewalls=fws)


@bp.route('/rack/delete/', methods=['GET', 'POST'])
@login_required
def rack_delete():

    rackid = request.args.get('rack')
    rack = Rack.query.get(rackid)

    if rack is None:
        flash(_('Rack was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Rack deleted: %s %s' % (rack.name,
                                           rack.location.longName())
    db.session.delete(rack)

    db.session.commit()
    flash(deleted_msg)
    audit.auditlog_delete_post('rack', data=rack.to_dict(), record_name=rack.name)

    return redirect(url_for('main.index'))


@bp.route('/rack/audit/', methods=['GET', 'POST'])
@login_required
def rack_audit():

    rackid = request.args.get('rack')

    rack = Rack.query.get(rackid)
    original_data = rack.to_dict()

    form = AuditRackForm(obj=rack)

    if rack is None:
        flash(_('Rack not found'))
        return redirect(request.referrer)

    if request.method == 'POST' and form.validate_on_submit():
        auditor = User.query.filter_by(username=current_user.username).first_or_404()

        if 'approved' in request.form:
            rack.audit_status = "approved"
        elif 'failed' in request.form:
            rack.audit_status = "failed"
        else:
            flash(_('Unknown auditor status'))
            return redirect(request.referrer)

        rack.audit_date = datetime.utcnow()
        rack.audit_comment = form.comment.data
        rack.auditor_id = auditor.id
        db.session.commit()
        audit.auditlog_update_post('rack', original_data=original_data, updated_data=rack.to_dict(), record_name=rack.name)

        flash(_(f'Your audit of rack {rack.name} have been saved.'))

        return redirect(url_for('main.rack_list'))

    else:
        from app.modules.server.models import Server

        servers = Server.query.filter(Server.rack_id == rack.id)
        switchs = Switch.query.filter(Switch.rack_id == rack.id)
        fws = Firewall.query.filter(Firewall.rack_id == rack.id)

        return render_template('rack.html', title=_(f'Audit Rack contents, {rack.name}'),
                               server_title=_('Servers'),
                               firewall_title=_('Firewalls'),
                               switch_title=_('Switches'),
                               form=form, servers=servers,
                               switchs=switchs, firewalls=fws)


@bp.route('/rack/qr/<int:id>', methods=['GET'])
@login_required
def rack_qr(id):

    if id is None:
        flash(_('Rack was not found, id not found!'))
        return redirect(url_for('main.index'))

    rack=None
    rack = Rack.query.get(id)

    if rack is None:
        flash(_('rack was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.rack_edit", rack=rack.id, _external=True)
    return render_template('rack_qr.html', title=_('QR Code'),
                           rack=rack, qr_data=qr_data)
