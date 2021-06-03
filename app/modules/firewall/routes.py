from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service
# from app.modules.firewall.models import Switch, SwitchPort
from app.modules.rack.models import Rack
from app.modules.network.models import Network
from app.modules.firewall.models import Firewall, FirewallPort
from app.modules.firewall.forms import FirewallForm, FirewallPortForm, FilterFirewallListForm
from flask_babel import _


@bp.route('/firewall/add', methods=['GET', 'POST'])
@login_required
def firewall_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = FirewallForm(formdata=request.form)

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.get(form.service.data)
        if service is None:
            flash('Service is required')
            return redirect(request.referrer)
        rack = Rack.query.get(form.rack.data)
        if rack is None:
            flash('Rack is required')
            return redirect(request.referrer)

        firewall = Firewall(name=form.name.data,
                            alias=form.alias.data,
                            ipaddress=form.ipaddress.data,
                            serial=form.serial.data,
                            manufacturer=form.manufacturer.data,
                            model=form.model.data,
                            status=form.status.data,
                            support_start=form.support_start.data,
                            support_end=form.support_end.data,
                            rack_position=form.rack_position.data,
                            comment=form.comment.data,
                            )

        firewall.service = service
        firewall.rack = rack
        db.session.add(firewall)
        db.session.commit()
        audit.auditlog_new_post('firewall', original_data=firewall.to_dict(), record_name=firewall.name)
        flash(_('New firewall is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('firewall.html', title=_('Add Firewall'),
                               form=form)


@bp.route('/firewall/edit/', methods=['GET', 'POST'])
@login_required
def firewall_edit():

    firewallid = request.args.get('firewall')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.firewall_delete', firewall=firewallid))
    if 'copy' in request.form:
        return redirect(url_for('main.firewall_copy', copy_from_firewall=firewallid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='firewall', module_id=firewallid))
    if 'ports' in request.form:
        return redirect(url_for('main.firewall_port_list', firewall=firewallid))

    firewall = Firewall.query.get(firewallid)
    original_data = firewall.to_dict()

    if firewall is None:
        render_template('service.html', title=_('Firewall is not defined'))

    form = FirewallForm(formdata=request.form, obj=firewall)

    if request.method == 'POST' and form.validate_on_submit():

        firewall.name = form.name.data
        firewall.alias = form.alias.data
        firewall.ipaddress = form.ipaddress.data
        firewall.serial = form.serial.data
        firewall.manufacturer = form.manufacturer.data
        firewall.model = form.model.data
        firewall.rack_id = form.rack.data
        firewall.service_id = form.service.data
        firewall.status = form.status.data
        firewall.support_start = form.support_start.data
        firewall.support_end = form.support_end.data
        firewall.rack_position = form.rack_position.data
        firewall.comment = form.comment.data
        db.session.commit()
        audit.auditlog_update_post('firewall', original_data=original_data, updated_data=firewall.to_dict(), record_name=firewall.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.service.data = firewall.service_id
        form.rack.data = firewall.rack_id
        return render_template('firewall.html', title=_('Edit Firewall'),
                               form=form)


@bp.route('/firewall/list/', methods=['GET', 'POST'])
@login_required
def firewall_list():
    from app.modules.server.models import Server

    page = request.args.get('page', 1, type=int)
    service_name = request.args.get('service')
    service = Service.query.filter_by(name=service_name).first()

    form = FilterFirewallListForm()

    if request.method == 'POST' and form.validate_on_submit():
        server = Server.query.get(form.server.data)
        rack = Rack.query.get(form.rack.data)

        if server is not None:
            # a server is connected to a firewall port not a firewall thus:
            # TODO
            firewall_ports = FirewallPort.query.filter_by(server_id=server.id).all()
        elif service is not None:
            firewalls = Firewall.query.filter_by(service_id=service.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif rack is not None:
            firewalls = Firewall.query.filter_by(rack_id=rack.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            firewalls = Firewall.query.order_by(Firewall.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    else:
        if service is not None:
            firewalls = Firewall.query.filter_by(service_id=service.id).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            firewalls = Firewall.query.order_by(Firewall.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.firewall_list', page=firewalls.next_num) \
        if firewalls.has_next else None
    prev_url = url_for('main.firewall_list', page=firewalls.prev_num) \
        if firewalls.has_prev else None

    return render_template('firewall.html', title=_('Firewall'),
                           firewalls=firewalls.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/firewall/delete/', methods=['GET', 'POST'])
@login_required
def firewall_delete():

    firewallid = request.args.get('firewall')
    firewall = Firewall.query.get(firewallid)

    if firewall is None:
        flash(_('Firewall was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Firewall deleted: %s\n' % (firewall.name)
    flash(deleted_msg)
    db.session.delete(firewall)
    db.session.commit()
    audit.auditlog_delete_post('firewall', data=firewall.to_dict(), record_name=firewall.name)

    return redirect(url_for('main.index'))


@bp.route('/firewall/port/add/', methods=['GET', 'POST'])
@login_required
def firewall_port_add():
    from app.modules.server.models import Server

    form = FirewallPortForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = FirewallPortForm(formdata=request.form)

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():

        firewallport = FirewallPort(name=form.name.data,
                                    server_if=form.server_if.data,
                                    comment=form.comment.data
                                    )
        firewall = Firewall.query.get(form.firewall.data)
        if firewall is not None:
            firewallport.firewall = firewall
        else:
            flash(_('Firewall is mandatory!'))
            return redirect(request.referrer)

        network = Network.query.get(form.network.data)
        if network is not None:
            firewallport.network = network

        if form.server.data is not None:
            server = Server.query.get(form.server.data)
            firewallport.server = server
        db.session.add(firewallport)
        db.session.commit()
        audit.auditlog_new_post('firewallport', original_data=firewallport.to_dict(), record_name=firewallport.name)
        flash(_('New firewallport is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('firewall.html', title=_('Add FirewallPort'),
                               form=form)


@bp.route('/firewall/port/edit/', methods=['GET', 'POST'])
@login_required
def firewall_port_edit():

    firewallportid = request.args.get('firewallport')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.firewall_port_delete', firewallport=firewallportid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='firewallport', module_id=firewallportid))

    firewallport = FirewallPort.query.get(firewallportid)
    original_data = firewallport.to_dict()

    if firewallport is None:
        flash(_('FirewallPort is not defined'))
        redirect(request.referrer)

    form = FirewallPortForm(formdata=request.form, obj=firewallport)

    if request.method == 'POST' and form.validate_on_submit():

        firewallport.name = form.name.data
        firewallport.firewall_id = form.firewall.data
        firewallport.server_id = form.server.data
        firewallport.server_if = form.server_if.data
        firewallport.network_id = form.network.data
        firewallport.comment = form.comment.data

        db.session.commit()
        audit.auditlog_update_post('firewallport', original_data=original_data, updated_data=firewallport.to_dict(), record_name=firewallport.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.firewall.data = firewallport.firewall_id
        form.server.data = firewallport.server_id

        return render_template('firewall.html', title=_('Edit FirewallPort'),
                               form=form)


@bp.route('/firewall/port/list/', methods=['GET', 'POST'])
@login_required
def firewall_port_list():
    from app.modules.server.models import Server

    page = request.args.get('page', 1, type=int)
    firewallid = request.args.get('firewall')
    serverid = request.args.get('serverid')

    server = None
    firewall = None

    if serverid is not None:
        server = Server.query.get(serverid)

    if firewallid is not None:
        firewall = Firewall.query.get(firewallid)

    form = FilterFirewallListForm()

    if request.method == 'POST' and form.validate_on_submit():
        server = Server.query.get(form.server.data)
        rack = Rack.query.get(form.rack.data)
        network = Rack.query.get(form.network.data)

        if server is not None:
            firewallports = FirewallPort.query.filter_by(server_id=server.id).all()
        elif rack is not None:
            firewallports = FirewallPort.query.filter_by(rack_id=rack).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif network is not None:
            firewallports = FirewallPort.query.filter_by(netowrk_id=network).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            firewallports = FirewallPort.query.order_by(Firewall.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
    else:

        if server is not None and firewall is not None:
            firewallports = FirewallPort.query.filter((FirewallPort.server_id == server.id),
                                                      (FirewallPort.firewall_id == firewall.id)).paginate(
                                                  page, current_app.config['POSTS_PER_PAGE'], False)
        elif server is not None:
            firewallports = FirewallPort.query.filter_by(server_id=server.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
        elif firewall is not None:
            firewallports = FirewallPort.query.filter_by(firewall_id=firewall.id).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
        else:
            firewallports = FirewallPort.query.order_by(FirewallPort.name).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.firewall_port_list', page=firewallports.next_num) \
        if firewallports.has_next else None
    prev_url = url_for('main.firewall_port_list', page=firewallports.prev_num) \
        if firewallports.has_prev else None

    return render_template('firewall.html', title=_('FirewallPort'),
                           firewallports=firewallports.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/firewall/port/delete/', methods=['GET', 'POST'])
@login_required
def firewall_port_delete():

    firewallportid = request.args.get('firewallport')
    firewallport = FirewallPort.query.get(firewallportid)

    if firewallport is None:
        flash(_('FirewallPort was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'FirewallPort deleted: %s\n' % (firewallport.name)
    flash(deleted_msg)
    db.session.delete(firewallport)
    db.session.commit()
    audit.auditlog_delete_post('firewallport', data=firewallport.to_dict(), record_name=firewallport.name)

    return redirect(url_for('main.index'))
