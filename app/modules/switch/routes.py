from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service, Location
from app.modules.switch.models import Switch
from app.modules.rack.models import Rack
from app.modules.switch.forms import SwitchForm
from flask_babel import _


@bp.route('/switch/add', methods=['GET', 'POST'])
@login_required
def switch_add():
    form = SwitchForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = SwitchForm(formdata=request.form)

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.get(form.service.data)
        if service is None:
            flash('Service is required')
            return redirect(request.referrer)
        location = Location.query.get(form.location.data)
        rack = Rack.query.get(form.rack.data)

        switch = Switch(name=form.name.data,
                        ipaddress=form.ipaddress.data,
                        status=form.status.data,
                        serial=form.serial.data,
                        model=form.model.data,
                        manufacturer=form.manufacturer.data,
                        comment=form.comment.data,
                        support_start=form.support_start.data,
                        support_end=form.support_end.data,
                        rack_position=form.rack_position.data
                        )

        switch.service = service
        switch.location = location
        switch.rack = rack
        db.session.add(switch)
        db.session.commit()
        audit.auditlog_new_post('switch', original_data=switch.to_dict(), record_name=switch.name)
        flash(_('New switch is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('switch.html', title=_('Add Switch'),
                               form=form)


@bp.route('/switch/edit/', methods=['GET', 'POST'])
@login_required
def switch_edit():

    switchid = request.args.get('switch')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.switch_delete', switch=switchid))
    if 'copy' in request.form:
        return redirect(url_for('main.switch_copy', copy_from_switch=switchid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='switch', module_id=switchid))

    switch = Switch.query.get(switchid)
    original_data = switch.to_dict()

    if switch is None:
        render_template('service.html', title=_('Switch is not defined'))

    form = SwitchForm(formdata=request.form, obj=switch)

    if request.method == 'POST' and form.validate_on_submit():

        switch.name = form.name.data
        switch.ipaddress = form.ipaddress.data
        switch.location_id = form.location.data
        switch.service_id = form.service.data
        switch.rack_id = form.rack.data
        switch.comment = form.comment.data
        switch.support_start = form.support_start.data
        switch.support_end = form.support_end.data
        switch.rack_position = form.rack_position.data

        db.session.commit()
        audit.auditlog_update_post('switch', original_data=original_data, updated_data=switch.to_dict(), record_name=switch.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.location.data = switch.location_id
        form.service.data = switch.service_id
        form.rack.data = switch.rack_id
        return render_template('switch.html', title=_('Edit Switch'),
                               form=form)


@bp.route('/switch/copy/', methods=['GET', 'POST'])
@login_required
def switch_copy():

    switchid = request.args.get('copy_from_switch')

    if 'cancel' in request.form:
        return redirect(request.referrer)

    copy_from_switch = Switch.query.get(switchid)

    form = SwitchForm(obj=copy_from_switch)
    form.service.data = copy_from_switch.service_id

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.id, service.name)]

    else:
        form.service.choices = [(s.id, s.name) for s in Service.query.all()]

    location_choices = []
    for l in Location.query.all():
        newloc = (l.id, l.longName())
        location_choices.append(newloc)
    form.location.choices = location_choices

    if copy_from_switch is None:
        render_template('service.html', title=_('Switch is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        switch = Switch(name=form.name.data,
                        status=form.status.data,
                        location=form.location.data)
        service = Service.query.get(form.service.data)
        switch.service = service
        db.session.add(switch)

        db.session.commit()
        audit.auditlog_new_post('switch', original_data=switch.to_dict(), record_name=switch.name)
        flash(_('Copied values from switch %s to %s.' % (copy_from_switch.name, switch.name)))

        return redirect(url_for('main.index'))

    else:
        return render_template('switch.html', title=_('Edit Switch'),
                               form=form)


@bp.route('/switch/list/', methods=['GET', 'POST'])
@login_required
def switch_list():

    page = request.args.get('page', 1, type=int)
    service_name = request.args.get('service')
    service = Service.query.filter_by(name=service_name).first()

    if service is not None:
        switchs = Switch.query.filter_by(service_id=service.id).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    else:
        switchs = Switch.query.order_by(Switch.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.switch_list', page=switchs.next_num) \
        if switchs.has_next else None
    prev_url = url_for('main.switch_list', page=switchs.prev_num) \
        if switchs.has_prev else None

    return render_template('switch.html', title=_('Switch'),
                           switchs=switchs.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/switch/delete/', methods=['GET', 'POST'])
@login_required
def switch_delete():

    switchid = request.args.get('switch')
    switch = Switch.query.get(switchid)

    if switch is None:
        flash(_('Switch was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Switch deleted: %s\n' % (switch.name)
    flash(deleted_msg)
    db.session.delete(switch)
    db.session.commit()
    audit.auditlog_delete_post('switch', data=switch.to_dict(), record_name=switch.name)

    return redirect(url_for('main.index'))
