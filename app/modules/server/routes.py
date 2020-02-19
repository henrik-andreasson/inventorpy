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
        form.service.choices = [(service.name, service.name)]

    else:
        form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    location_choices = []
    for l in Location.query.all():
        formatedloc = "%s-%s-%s-%s" % (l.place, l.facillity, l.area, l.position)
        print("loc: %s:%s" % (l.id, formatedloc))
        newloc = (formatedloc, formatedloc)
        location_choices.append(newloc)
    form.location.choices = location_choices
#    form.location.choices = [(l.id, l.city) for l in Location.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.filter_by(name=form.service.data).first()
#        for field in ['hostname', 'ipaddress', 'netmask', 'gateway', 'memory', 'cpu', 'location', 'service_id', 'status']:
#            setattr(self, field, data[field])

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

    server = Server.query.get(serverid)

    form = ServerForm(obj=server)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.name, service.name)]

    else:
        form.service.choices = [(s.name, s.name) for s in Service.query.all()]

    location_choices = []
    for l in Location.query.all():
        formatedloc = "%s-%s-%s-%s-%s" % (l.place, l.facillity, l.area, l.position, l.type)
        print("loc: %s:%s" % (l.id, formatedloc))
        newloc = (formatedloc, formatedloc)
        location_choices.append(newloc)
    form.location.choices = location_choices

    if server is None:
        render_template('service.html', title=_('Server is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        string_from = '%s\t%s\t%s\t@%s\n' % (server.hostname, server.ipaddress,
                                             server.location, server.service)
        service = Service.query.filter_by(name=form.service.data).first()
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

        if current_app.config['ROCKET_ENABLED']:
            string_to = '%s\t%s\t%s\t@%s\n' % (server.start, server.stop,
                                               server.service, server.username)
            rocket = RocketChat(current_app.config['ROCKET_USER'],
                                current_app.config['ROCKET_PASS'],
                                server_url=current_app.config['ROCKET_URL'])
            rocket.chat_post_message('edit of server from: \n%s\nto:\n%s\nby: %s' % (
                                 string_from, string_to, current_user.username),
                                 channel=current_app.config['ROCKET_CHANNEL']
                                 ).json()

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

    deleted_msg = 'Server deleted: %s\t%s\t%s\t@%s\n' % (server.start, server.stop,
                                                       server.service.name,
                                                       server.username)
    if current_app.config['ROCKET_ENABLED']:
        rocket = RocketChat(current_app.config['ROCKET_USER'],
                            current_app.config['ROCKET_PASS'],
                            server_url=current_app.config['ROCKET_URL'])
        rocket.chat_post_message('server deleted: \n%s\nto:\n%s\nby: %s' % (
                             deleted_msg, current_user.username),
                             channel=current_app.config['ROCKET_CHANNEL']
                             ).json()
    flash(deleted_msg)
    db.session.delete(server)
    db.session.commit()

    return redirect(url_for('main.index'))
