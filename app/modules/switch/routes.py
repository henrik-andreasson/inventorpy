from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service
from app.modules.switch.models import Switch, SwitchPort
from app.modules.rack.models import Rack
from app.modules.network.models import Network
from app.modules.switch.forms import SwitchForm, SwitchPortForm, FilterSwitchListForm
from flask_babel import _


@bp.route('/switch/add', methods=['GET', 'POST'])
@login_required
def switch_add():
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
        rack = Rack.query.get(form.rack.data)

        switch = Switch(name=form.name.data,
                        alias=form.alias.data,
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
        switch.rack = rack
        db.session.add(switch)
        db.session.commit()
        audit.auditlog_new_post(
            'switch', original_data=switch.to_dict(), record_name=switch.name)
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
    if 'ports' in request.form:
        return redirect(url_for('main.switch_port_list', switch=switchid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.switch_qr', id=switchid))

    switch = Switch.query.get(switchid)
    original_data = switch.to_dict()

    if switch is None:
        render_template('service.html', title=_('Switch is not defined'))

    form = SwitchForm(formdata=request.form, obj=switch)

    if request.method == 'POST' and form.validate_on_submit():

        switch.name = form.name.data
        switch.alias = form.alias.data
        switch.ipaddress = form.ipaddress.data
        switch.service_id = form.service.data
        switch.rack_id = form.rack.data
        switch.comment = form.comment.data
        switch.support_start = form.support_start.data
        switch.support_end = form.support_end.data
        switch.rack_position = form.rack_position.data

        db.session.commit()
        audit.auditlog_update_post('switch', original_data=original_data,
                                   updated_data=switch.to_dict(), record_name=switch.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.service.data = switch.service_id
        form.rack.data = switch.rack_id
        return render_template('switch.html', title=_('Edit Switch'),
                               form=form)


@bp.route('/switch/list/', methods=['GET', 'POST'])
@login_required
def switch_list():
    from app.modules.server.models import Server

    page = request.args.get('page', 1, type=int)
    service_name = request.args.get('service')
    service = Service.query.filter_by(name=service_name).first()

    form = FilterSwitchListForm()

    if request.method == 'POST' and form.validate_on_submit():
        server = Server.query.get(form.server.data)
        rack = Rack.query.get(form.rack.data)

        if server is not None:
            # a server is connected to a switch port not a switch thus:
            # TODO
            switch_ports = SwitchPort.query.filter_by(
                server_id=server.id).all()
        elif service is not None:
            switchs = Switch.query.filter_by(service_id=service.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif rack is not None:
            switchs = Switch.query.filter_by(rack_id=rack.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            switchs = Switch.query.order_by(Switch.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    else:
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
                           prev_url=prev_url, form=form)


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
    audit.auditlog_delete_post(
        'switch', data=switch.to_dict(), record_name=switch.name)

    return redirect(url_for('main.index'))


@bp.route('/switch/port/add/', methods=['GET', 'POST'])
@login_required
def switch_port_add():
    from app.modules.server.models import Server

    form = SwitchPortForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = SwitchPortForm(formdata=request.form)

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():

        switchport = SwitchPort(name=form.name.data,
                                server_if=form.server_if.data,
                                comment=form.comment.data
                                )
        switch = Switch.query.get(form.switch.data)
        if switch is not None:
            switchport.switch = switch
        else:
            flash(_('Switch is mandatory!'))
            return redirect(request.referrer)

        network = Network.query.get(form.network.data)
        if network is not None:
            switchport.network = network

        if form.server.data is not None:
            server = Server.query.get(form.server.data)
            switchport.server = server
        db.session.add(switchport)
        db.session.commit()
        audit.auditlog_new_post(
            'switchport', original_data=switchport.to_dict(), record_name=switchport.name)
        flash(_('New switchport is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('switch.html', title=_('Add SwitchPort'),
                               form=form)


@bp.route('/switch/port/edit/', methods=['GET', 'POST'])
@login_required
def switch_port_edit():

    switchportid = request.args.get('switchport')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.switch_port_delete', switchport=switchportid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='switchport', module_id=switchportid))

    switchport = SwitchPort.query.get(switchportid)
    original_data = switchport.to_dict()

    if switchport is None:
        flash(_('SwitchPort is not defined'))
        redirect(request.referrer)

    form = SwitchPortForm(formdata=request.form, obj=switchport)

    if request.method == 'POST' and form.validate_on_submit():

        switchport.name = form.name.data
        switchport.switch_id = form.switch.data
        switchport.server_id = form.server.data
        switchport.server_if = form.server_if.data
        switchport.network_id = form.network.data
        switchport.comment = form.comment.data

        db.session.commit()
        audit.auditlog_update_post('switchport', original_data=original_data,
                                   updated_data=switchport.to_dict(), record_name=switchport.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.switch.data = switchport.switch_id
        form.server.data = switchport.server_id

        return render_template('switch.html', title=_('Edit SwitchPort'),
                               form=form)


@bp.route('/switch/port/list/', methods=['GET', 'POST'])
@login_required
def switch_port_list():
    from app.modules.server.models import Server

    page = request.args.get('page', 1, type=int)
    switchid = request.args.get('switch')
    serverid = request.args.get('serverid')

    server = None
    if serverid is not None:
        server = Server.query.get(serverid)

    switch = None
    if switchid is not None:
        switch = Switch.query.get(switchid)

    form = FilterSwitchListForm()

    if request.method == 'POST' and form.validate_on_submit():
        server = Server.query.get(form.server.data)
        rack = Rack.query.get(form.rack.data)
        network = Rack.query.get(form.network.data)

        if server is not None:
            switchports = SwitchPort.query.filter_by(server_id=server.id).all()
        elif rack is not None:
            switchports = SwitchPort.query.filter_by(rack_id=rack).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif network is not None:
            switchports = SwitchPort.query.filter_by(netowrk_id=network).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            switchports = SwitchPort.query.order_by(SwitchPort.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
    else:

        if server is not None and switch is not None:
            switchports = SwitchPort.query.filter((SwitchPort.server_id == server.id),
                                                  (SwitchPort.switch_id == switch.id)).paginate(
                                                  page, current_app.config['POSTS_PER_PAGE'], False)
        elif server is not None:
            switchports = SwitchPort.query.filter_by(server_id=server.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif switch is not None:
            switchports = SwitchPort.query.filter_by(switch_id=switch.id).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            switchports = SwitchPort.query.order_by(SwitchPort.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.switch_port_list', page=switchports.next_num) \
        if switchports.has_next else None
    prev_url = url_for('main.switch_port_list', page=switchports.prev_num) \
        if switchports.has_prev else None

    return render_template('switch.html', title=_('SwitchPort'),
                           switchports=switchports.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/switch/port/delete/', methods=['GET', 'POST'])
@login_required
def switch_port_delete():

    switchportid = request.args.get('switchport')
    switchport = SwitchPort.query.get(switchportid)

    if switchport is None:
        flash(_('SwitchPort was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'SwitchPort deleted: %s\n' % (switchport.name)
    flash(deleted_msg)
    db.session.delete(switchport)
    db.session.commit()
    audit.auditlog_delete_post(
        'switchport', data=switchport.to_dict(), record_name=switchport.name)

    return redirect(url_for('main.index'))


@bp.route('/switch/qr/<int:id>', methods=['GET'])
@login_required
def switch_qr(id):

    if id is None:
        flash(_('switch was not found, id not found!'))
        return redirect(url_for('main.index'))

    switch = None
    switch = Switch.query.get(id)

    if switch is None:
        flash(_('switch was not found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.switch_edit", switch=switch.id, _external=True)
    return render_template('switch_qr.html', title=_('QR Code'),
                           switch=switch, qr_data=qr_data)
