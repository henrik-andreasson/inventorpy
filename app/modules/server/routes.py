from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Service, Location
from app.modules.server.models import Server
from app.modules.server.forms import ServerForm
from rocketchat_API.rocketchat import RocketChat
from flask_babel import _


@bp.route('/server/add', methods=['GET', 'POST'])
@login_required
def server_add():
    form = ServerForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = ServerForm(formdata=request.form)

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

    ip = request.args.get('ip')
    if ip:
        form.ipaddress.data = ip

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.get(form.service.data)

        server = Server(hostname=form.hostname.data,
                        ipaddress=form.ipaddress.data,
                        status=form.status.data,
                        netmask=form.netmask.data,
                        gateway=form.gateway.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        location=form.location.data)
        server.service = service
        db.session.add(server)
        db.session.commit()
        flash(_('New server is now posted!'))

        return redirect(url_for('main.index'))

    else:

        servers = Server.query.order_by(Server.id.desc()).limit(10)
        return render_template('server.html', title=_('Add Server'),
                               form=form, servers=servers)


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

    server = Server.query.get(serverid)

    form = ServerForm(obj=server)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
    else:
        form.service.choices = [(s.id, s.name) for s in Service.query.all()]

    location_choices = []
    for l in Location.query.all():
        newloc = (l.id, l.longName())
        location_choices.append(newloc)
    form.location.choices = location_choices
    form.service.data = server.service_id

    if server is None:
        render_template('service.html', title=_('Server is not defined'))

    if request.method == 'POST' and form.validate_on_submit():

        service = Service.query.get(form.service.data)
        server.hostname = form.hostname.data
        server.ipaddress = form.ipaddress.data
        server.netmask = form.netmask.data
        server.gateway = form.gateway.data
        server.memory = form.memory.data
        server.cpu = form.cpu.data
        server.location = form.location.data
        server.service = service

        db.session.commit()
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
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
        form.service.choices = [(service.di, service.name)]

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
                        ipaddress=form.ipaddress.data,
                        status=form.status.data,
                        netmask=form.netmask.data,
                        gateway=form.gateway.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        location=form.location.data)
        service = Service.query.get(form.service.data)
        server.service = service
        db.session.add(server)
        db.session.commit()
        flash(_('Copied values from server %s to %s.' % (copy_from_server.hostname, server.hostname)))

        return redirect(url_for('main.index'))

    else:
        return render_template('server.html', title=_('Edit Server'),
                               form=form)


@bp.route('/server/list/', methods=['GET', 'POST'])
@login_required
def server_list():

    page = request.args.get('page', 1, type=int)

    servers = Server.query.order_by(Server.hostname).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.server_list', page=servers.next_num) \
        if servers.has_next else None
    prev_url = url_for('main.server_list', page=servers.prev_num) \
        if servers.has_prev else None

    return render_template('server.html', title=_('Server'),
                           servers=servers.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/server/delete/', methods=['GET', 'POST'])
@login_required
def server_delete():

    serverid = request.args.get('server')
    server = Server.query.get(serverid)

    if server is None:
        flash(_('Server was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Server deleted: %s@%s\n' % (server.hostname,
                                               server.service.name)
    flash(deleted_msg)
    db.session.delete(server)
    db.session.commit()

    return redirect(url_for('main.index'))
