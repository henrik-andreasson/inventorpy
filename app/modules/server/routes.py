from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service, Location
from app.modules.server.models import Server, VirtualServer
from app.modules.rack.models import Rack
from app.modules.server.forms import ServerForm, FilterServerListForm, VirtualServerForm, FilterVirtualServerListForm
from flask_babel import _
from sqlalchemy import desc, asc
from app.api.errors import bad_request


@bp.route('/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    form = ServerForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = ServerForm(formdata=request.form)

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

        server = Server(hostname=form.hostname.data,
                        role=form.role.data,
                        ipaddress=form.ipaddress.data,
                        status=form.status.data,
                        network_id=form.network.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        psu=form.psu.data,
                        hd=form.hd.data,
                        os_name=form.os_name.data,
                        os_version=form.os_version.data,
                        serial=form.serial.data,
                        model=form.model.data,
                        manufacturer=form.manufacturer.data,
                        comment=form.comment.data,
                        support_start=form.support_start.data,
                        support_end=form.support_end.data,
                        rack_position=form.rack_position.data,
                        environment=form.environment.data
                        )

        server.service = service
        server.location = location
        server.rack = rack
        db.session.add(server)
        db.session.commit()
        audit.auditlog_new_post('server', original_data=server.to_dict(), record_name=server.hostname)
        flash(_('New server is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('server.html', title=_('Add Server'),
                               form=form)


@bp.route('/server/edit/', methods=['GET', 'POST'])
@login_required
def server_edit():

    serverid = request.args.get('server')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.server_delete', server=serverid))
    if 'copy' in request.form:
        return redirect(url_for('main.server_copy', copy_from_server=serverid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='server', module_id=serverid))
    if 'hsm' in request.form:
        return redirect(url_for('main.hsm_pcicard_list', serverid=serverid))
    if 'switchport' in request.form:
        return redirect(url_for('main.switch_port_list', serverid=serverid))

    server = Server.query.get(serverid)
    original_data = server.to_dict()

    if server is None:
        render_template('service.html', title=_('Server is not defined'))

    form = ServerForm(formdata=request.form, obj=server)

    if request.method == 'POST' and form.validate_on_submit():

        server.hostname = form.hostname.data
        server.role = form.role.data
        server.ipaddress = form.ipaddress.data
        server.network_id = form.network.data
        server.memory = form.memory.data
        server.cpu = form.cpu.data
        server.service_id = form.service.data
        server.rack_id = form.rack.data
        server.comment = form.comment.data
        server.support_start = form.support_start.data
        server.support_end = form.support_end.data
        server.rack_position = form.rack_position.data
        server.environment = form.environment.data
        server.virtual_host = form.virtual_host.data

        db.session.commit()
        audit.auditlog_update_post('server', original_data=original_data, updated_data=server.to_dict(), record_name=server.hostname)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.network.data = server.network_id
        form.service.data = server.service_id
        form.rack.data = server.rack_id
        return render_template('server.html', title=_('Edit Server'),
                               form=form)


@bp.route('/server/copy/', methods=['GET', 'POST'])
@login_required
def server_copy():

    serverid = request.args.get('copy_from_server')

    if 'cancel' in request.form:
        return redirect(request.referrer)

    copy_from_server = Server.query.get(serverid)

    form = ServerForm(obj=copy_from_server)
    form.service.data = copy_from_server.service_id

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

    if copy_from_server is None:
        render_template('service.html', title=_('Server is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        server = Server(hostname=form.hostname.data,
                        role=form.role.data,
                        ipaddress=form.ipaddress.data,
                        status=form.status.data,
                        network_id=form.network.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        virtual_host=form.virtual_host.data,
                        location=form.location.data)
        service = Service.query.get(form.service.data)
        server.service = service
        db.session.add(server)

        db.session.commit()
        audit.auditlog_new_post('server', original_data=server.to_dict(), record_name=server.hostname)
        flash(_('Copied values from server %s to %s.' % (copy_from_server.hostname, server.hostname)))

        return redirect(url_for('main.index'))

    else:
        return render_template('server.html', title=_('Edit Server'),
                               form=form)


@bp.route('/server/list/', methods=['GET', 'POST'])
@login_required
def server_list():

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'hostname')
    order = request.args.get('order', 'asc')
    server_vars = list(vars(Server).keys())

    if sort not in server_vars:
        flash(_('No such varibale to sort by %s' % sort))
        return redirect(url_for('main.index'))

    if order not in ['asc', 'desc']:
        flash(_('Bad order to sort by'))
        return redirect(url_for('main.index'))

    sortstr = "{}(Server.{})".format(order, sort)
    form = FilterServerListForm()

    environment = None
    service = None

    if request.method == 'POST' and form.validate_on_submit():
        service_id = form.service.data
        rack_id = form.rack.data
        environment = form.environment.data
        service = Service.query.filter_by(id=service_id).first()
        rack = Rack.query.get(rack_id)
    else:
        service_name = request.args.get('service')
        service = Service.query.filter_by(name=service_name).first()
        environment = request.args.get('environment')
        rack_id = request.args.get('rack_id')
        rack = Rack.query.get(rack_id)

    input_search_query = []
    if service is not None:
        print("service: {}".format(service.name))
        input_search_query.append('(Server.service_id == service.id)')
    if environment is not None and environment != "all":
        print("env: {}".format(environment))
        input_search_query.append('(Server.environment == environment)')
    if rack is not None:
        print("env: {}".format(rack.name))
        input_search_query.append('(Server.rack_id == rack.id)')

    if len(input_search_query) < 1:
        servers = Server.query.order_by(eval(sortstr)).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    else:
        query = " & ".join(input_search_query)
        print("query: {}".format(query))
        servers = Server.query.filter(eval(query)).order_by(eval(sortstr)).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.server_list', page=servers.next_num) \
        if servers.has_next else None
    prev_url = url_for('main.server_list', page=servers.prev_num) \
        if servers.has_prev else None

    return render_template('server.html', title=_('Server'),
                           servers=servers.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/server/delete/', methods=['GET', 'POST'])
@login_required
def server_delete():

    serverid = request.args.get('server')
    server = Server.query.get(serverid)

    if server is None:
        flash(_('Server was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Server deleted: %s\n' % (server.hostname)
    flash(deleted_msg)
    db.session.delete(server)
    db.session.commit()
    audit.auditlog_delete_post('server', data=server.to_dict(), record_name=server.hostname)

    return redirect(url_for('main.index'))


@bp.route('/virtual_server/add', methods=['GET', 'POST'])
@login_required
def virtual_server_add():
    form = VirtualServerForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = VirtualServerForm(formdata=request.form)

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.get(form.service.data)
        if service is None:
            flash('Service is required')
            return redirect(request.referrer)

        virtual_server = VirtualServer(hostname=form.hostname.data,
                                       role=form.role.data,
                                       ipaddress=form.ipaddress.data,
                                       status=form.status.data,
                                       network_id=form.network.data,
                                       memory=form.memory.data,
                                       cpu=form.cpu.data,
                                       hd=form.hd.data,
                                       os_name=form.os_name.data,
                                       os_version=form.os_version.data,
                                       comment=form.comment.data,
                                       environment=form.environment.data)

        virtual_server.service = service
        db.session.add(virtual_server)
        db.session.commit()
        audit.auditlog_new_post('virtual_server', original_data=virtual_server.to_dict(), record_name=virtual_server.hostname)
        flash(_('New virtual_server is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('server.html', title=_('Add VirtualServer'),
                               form=form)


@bp.route('/virtual_server/edit/', methods=['GET', 'POST'])
@login_required
def virtual_server_edit():

    virtual_serverid = request.args.get('virtual_server')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.virtual_server_delete', virtual_server=virtual_serverid))
    if 'copy' in request.form:
        return redirect(url_for('main.virtual_server_copy', copy_from_virtual_server=virtual_serverid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='virtual_server', module_id=virtual_serverid))
    if 'hsm' in request.form:
        return redirect(url_for('main.hsm_pcicard_list', virtual_serverid=virtual_serverid))
    if 'switchport' in request.form:
        return redirect(url_for('main.switch_port_list', virtual_serverid=virtual_serverid))

    virtual_server = VirtualServer.query.get(virtual_serverid)
    original_data = virtual_server.to_dict()

    if virtual_server is None:
        render_template('service.html', title=_('VirtualServer is not defined'))

    form = VirtualServerForm(formdata=request.form, obj=virtual_server)

    if request.method == 'POST' and form.validate_on_submit():

        virtual_server.hostname = form.hostname.data
        virtual_server.role = form.role.data
        virtual_server.ipaddress = form.ipaddress.data
        virtual_server.network_id = form.network.data
        virtual_server.memory = form.memory.data
        virtual_server.cpu = form.cpu.data
        virtual_server.service_id = form.service.data
        virtual_server.comment = form.comment.data
        virtual_server.environment = form.environment.data

        db.session.commit()
        audit.auditlog_update_post('virtual_server', original_data=original_data, updated_data=virtual_server.to_dict(), record_name=virtual_server.hostname)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.network.data = virtual_server.network_id
        form.service.data = virtual_server.service_id
        form.status.data = virtual_server.status
        form.hosting_server.data = virtual_server.hosting_server_id

        return render_template('server.html', title=_('Edit VirtualServer'),
                               form=form)


@bp.route('/virtual_server/copy/', methods=['GET', 'POST'])
@login_required
def virtual_server_copy():

    virtual_serverid = request.args.get('copy_from_virtual_server')

    if 'cancel' in request.form:
        return redirect(request.referrer)

    copy_from_virtual_server = VirtualServer.query.get(virtual_serverid)

    form = VirtualServerForm(obj=copy_from_virtual_server)
    form.service.data = copy_from_virtual_server.service_id

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

    if copy_from_virtual_server is None:
        render_template('service.html', title=_('VirtualServer is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        virtual_server = VirtualServer(hostname=form.hostname.data,
                                       role=form.role.data,
                                       ipaddress=form.ipaddress.data,
                                       status=form.status.data,
                                       network_id=form.network.data,
                                       memory=form.memory.data,
                                       cpu=form.cpu.data)
        service = Service.query.get(form.service.data)
        virtual_server.service = service
        db.session.add(virtual_server)

        db.session.commit()
        audit.auditlog_new_post('virtual_server', original_data=virtual_server.to_dict(), record_name=virtual_server.hostname)
        flash(_('Copied values from virtual_server %s to %s.' % (copy_from_virtual_server.hostname, virtual_server.hostname)))

        return redirect(url_for('main.index'))

    else:
        return render_template('server.html', title=_('Edit VirtualServer'),
                               form=form)


@bp.route('/virtual_server/list/', methods=['GET', 'POST'])
@login_required
def virtual_server_list():

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'hostname')
    order = request.args.get('order', 'asc')
    virtual_server_vars = list(vars(VirtualServer).keys())

    if sort not in virtual_server_vars:
        flash(_('No such varibale to sort by %s' % sort))
        return redirect(url_for('main.index'))

    if order not in ['asc', 'desc']:
        flash(_('Bad order to sort by'))
        return redirect(url_for('main.index'))

    sortstr = "{}(VirtualServer.{})".format(order, sort)
    form = FilterVirtualServerListForm()

    environment = None
    service = None

    if request.method == 'POST' and form.validate_on_submit():
        service_id = form.service.data
        environment = form.environment.data
        service = Service.query.filter_by(id=service_id).first()
    else:
        service_name = request.args.get('service')
        service = Service.query.filter_by(name=service_name).first()
        environment = request.args.get('environment')

    input_search_query = []
    if service is not None:
        print("service: {}".format(service.name))
        input_search_query.append('(VirtualServer.service_id == service.id)')
    if environment is not None and environment != "all":
        print("env: {}".format(environment))
        input_search_query.append('(VirtualServer.environment == environment)')

    if len(input_search_query) < 1:
        virtual_servers = VirtualServer.query.order_by(eval(sortstr)).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    else:
        query = " & ".join(input_search_query)
        print("query: {}".format(query))
        virtual_servers = VirtualServer.query.filter(eval(query)).order_by(eval(sortstr)).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.virtual_server_list', page=virtual_servers.next_num) \
        if virtual_servers.has_next else None
    prev_url = url_for('main.virtual_server_list', page=virtual_servers.prev_num) \
        if virtual_servers.has_prev else None

    return render_template('server.html', title=_('VirtualServer'),
                           virtual_servers=virtual_servers.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/virtual_server/delete/', methods=['GET', 'POST'])
@login_required
def virtual_server_delete():

    virtual_serverid = request.args.get('virtual_server')
    virtual_server = VirtualServer.query.get(virtual_serverid)

    if virtual_server is None:
        flash(_('VirtualServer was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'VirtualServer deleted: %s\n' % (virtual_server.hostname)
    flash(deleted_msg)
    db.session.delete(virtual_server)
    db.session.commit()
    audit.auditlog_delete_post('virtual_server', data=virtual_server.to_dict(), record_name=virtual_server.hostname)

    return redirect(url_for('main.index'))
