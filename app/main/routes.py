from flask import render_template, flash, redirect, url_for, request, g, current_app
from app.modules.server.routes import virtual_server_add
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db, audit
from app.main.forms import EditProfileForm, ServiceForm, LocationForm, SearchForm
from app.models import User, Service, Location, Audit
from app.modules.hsm.models import HsmDomain, HsmPed, HsmPin, HsmPciCard, HsmPedUpdates, HsmBackupUnit
from app.modules.safe.models import Safe, Compartment
from app.modules.rack.models import Rack
from app.modules.server.models import Server, VirtualServer
from app.modules.network.models import Network
from app.modules.firewall.models import Firewall
from app.modules.pc.models import Pc
from app.modules.switch.models import Switch, SwitchPort
from app.main import bp
from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    users = User.query.order_by(User.username).limit(10)
    servers = Server.query.order_by(Server.hostname).limit(10)
    locations = Location.query.order_by(Location.place).limit(10)
    services = Service.query.order_by(Service.name).limit(10)
    hsmdomains = HsmDomain.query.order_by(HsmDomain.name).limit(10)
    hsmpeds = HsmPed.query.order_by(HsmPed.keysn).limit(10)
    hsmpins = HsmPin.query.order_by(HsmPin.id).limit(10)
    networks = Network.query.order_by(Network.name).limit(10)
    safes = Safe.query.order_by(Safe.name).limit(10)
    compartments = Compartment.query.order_by(Compartment.name).limit(10)
    hsmpcicards = HsmPciCard.query.order_by(HsmPciCard.serial).limit(10)
    hsmbackupunits = HsmBackupUnit.query.order_by(
        HsmBackupUnit.serial).limit(10)
    racks = Rack.query.order_by(Rack.name).limit(10)
    hsmpedupdates = HsmPedUpdates.query.order_by(HsmPedUpdates.id).limit(10)
    switches = Switch.query.order_by(Switch.id).limit(10)
    firewalls = Firewall.query.order_by(Firewall.id).limit(10)

    return render_template('index.html', title=_('Explore'),
                           servers=servers, locations=locations,
                           services=services, hsmdomains=hsmdomains,
                           hsmpeds=hsmpeds, hsmpins=hsmpins,
                           networks=networks, safes=safes, users=users,
                           compartments=compartments, hsmpcicards=hsmpcicards,
                           racks=racks, hsmpedupdates=hsmpedupdates,
                           hsmbackupunits=hsmbackupunits,
                           switches=switches, firewalls=firewalls)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    keyword = request.args.get('keyword')
    form = SearchForm()
    if keyword is None:
        if 'keyword' in request.form:
            keyword = form.keyword.data

    users = User.query.filter(User.username.like(f"%{keyword}%") |
        User.email.like(f"%{keyword}%") |
        User.role.like(f"%{keyword}%") |
        User.about_me.like(f"%{keyword}%")
    ).order_by(User.username).all()

    servers = Server.query.filter(Server.hostname.like(f"%{keyword}%") |
       Server.role.like(f"%{keyword}%") |
       Server.status.like(f"%{keyword}%") |
       Server.ipaddress.like(f"%{keyword}%") |
       Server.memory.like(f"%{keyword}%") |
       Server.cpu.like(f"%{keyword}%") |
       Server.os_name.like(f"%{keyword}%") |
       Server.os_version.like(f"%{keyword}%") |
       Server.comment.like(f"%{keyword}%") |
       Server.environment.like(f"%{keyword}%")
    ).order_by(Server.hostname).all()

    virtserv = VirtualServer.query.filter(VirtualServer.hostname.like(f"%{keyword}%") |
        VirtualServer.role.like(f"%{keyword}%") |
        VirtualServer.status.like(f"%{keyword}%") |
        VirtualServer.ipaddress.like(f"%{keyword}%") |
        VirtualServer.memory.like(f"%{keyword}%") |
        VirtualServer.cpu.like(f"%{keyword}%") |
        VirtualServer.os_name.like(f"%{keyword}%") |
        VirtualServer.os_version.like(f"%{keyword}%") |
        VirtualServer.comment.like(f"%{keyword}%") |
        VirtualServer.environment.like(f"%{keyword}%")
    ).order_by(VirtualServer.hostname).all()

    networks = Network.query.filter(Network.name.like(f"%{keyword}%") |
            Network.network.like(f"%{keyword}%") |
            Network.environment.like(f"%{keyword}%") |
            Network.netmask.like(f"%{keyword}%") |
            Network.gateway.like(f"%{keyword}%")
        ).order_by(Network.name).all()

    firewalls = Firewall.query.filter(Firewall.name.like(f"%{keyword}%") |
            Firewall.alias.like(f"%{keyword}%") |
            Firewall.ipaddress.like(f"%{keyword}%") |
            Firewall.model.like(f"%{keyword}%") |
            Firewall.status.like(f"%{keyword}%") |
            Firewall.support_start.like(f"%{keyword}%") |
            Firewall.support_end.like(f"%{keyword}%") |
            Firewall.comment.like(f"%{keyword}%") |
            Firewall.serial.like(f"%{keyword}%")
        ).order_by(Firewall.name).all()

    hsmdomains = HsmDomain.query.filter(HsmDomain.name.like(f"%{keyword}%")
            ).order_by(HsmDomain.name).all()

    hsmpeds = HsmPed.query.filter(HsmPed.type.like(f"%{keyword}%") |
                HsmPed.keyno.like(f"%{keyword}%") |
                HsmPed.keysn.like(f"%{keyword}%") |
                HsmPed.comment.like(f"%{keyword}%")
            ).order_by(HsmPed.type).all()

    hsmpcicards = HsmPciCard.query.filter(HsmPciCard.name.like(f"%{keyword}%") |
                HsmPciCard.serial.like(f"%{keyword}%") |
                HsmPciCard.fbno.like(f"%{keyword}%") |
                HsmPciCard.model.like(f"%{keyword}%") |
                HsmPciCard.manufacturedate.like(f"%{keyword}%") |
                HsmPciCard.status.like(f"%{keyword}%") |
                HsmPciCard.support_start.like(f"%{keyword}%") |
                HsmPciCard.support_end.like(f"%{keyword}%") |
                HsmPciCard.contract.like(f"%{keyword}%") |
                HsmPciCard.comment.like(f"%{keyword}%")
            ).order_by(HsmPciCard.name).all()

    hsmbackupunits = HsmBackupUnit.query.filter(HsmBackupUnit.name.like(f"%{keyword}%") |
                    HsmBackupUnit.serial.like(f"%{keyword}%") |
                    HsmBackupUnit.model.like(f"%{keyword}%") |
                    HsmBackupUnit.manufacturedate.like(f"%{keyword}%") |
                    HsmBackupUnit.comment.like(f"%{keyword}%")
                ).order_by(HsmBackupUnit.name).all()

    pcs = Pc.query.filter(Pc.name.like(f"%{keyword}%") |
                            Pc.serial.like(f"%{keyword}%") |
                            Pc.memory.like(f"%{keyword}%") |
                            Pc.model.like(f"%{keyword}%") |
                            Pc.manufacturer.like(f"%{keyword}%") |
                            Pc.status.like(f"%{keyword}%") |
                            Pc.cpu.like(f"%{keyword}%") |
                            Pc.hd.like(f"%{keyword}%") |
                            Pc.os_name.like(f"%{keyword}%") |
                            Pc.os_version.like(f"%{keyword}%") |
                            Pc.support_start.like(f"%{keyword}%") |
                            Pc.support_end.like(f"%{keyword}%") |
                            Pc.environment.like(f"%{keyword}%") |
                            Pc.comment.like(f"%{keyword}%")
                        ).order_by(Pc.name).all()

    racks = Rack.query.filter(Rack.name.like(f"%{keyword}%") |
                            Rack.comment.like(f"%{keyword}%")
                        ).order_by(Rack.name).all()


    safes = Safe.query.filter(Safe.name.like(f"%{keyword}%") |
            Safe.status.like(f"%{keyword}%") |
            Safe.comment.like(f"%{keyword}%")
        ).order_by(Safe.name).all()

    compartments = Compartment.query.filter(Compartment.name.like(f"%{keyword}%") |
            Compartment.audit_date.like(f"%{keyword}%") |
            Compartment.comment.like(f"%{keyword}%")
        ).order_by(Compartment.name).all()

    switches = Switch.query.filter(Switch.name.like(f"%{keyword}%") |
                Switch.alias.like(f"%{keyword}%") |
                Switch.support_start.like(f"%{keyword}%") |
                Switch.support_end.like(f"%{keyword}%") |
                Switch.manufacturer.like(f"%{keyword}%") |
                Switch.serial.like(f"%{keyword}%") |
                Switch.ipaddress.like(f"%{keyword}%") |
                Switch.model.like(f"%{keyword}%") |
                Switch.status.like(f"%{keyword}%") |
                Switch.comment.like(f"%{keyword}%")
            ).order_by(Switch.name).all()

    switchports = SwitchPort.query.filter(SwitchPort.name.like(f"%{keyword}%") |
                SwitchPort.comment.like(f"%{keyword}%")
            ).order_by(SwitchPort.name).all()

    return render_template('search.html', title=_('Search'),
                           users=users, servers=servers,
                           virtual_servers=virtserv,
                           networks=networks,
                           firewalls=firewalls,
                           hsmdomains=hsmdomains,
                           hsmpeds=hsmpeds,
                           hsmpcicards=hsmpcicards,
                           hsmbackupunits=hsmbackupunits,
                           pcs=pcs,
                           racks=racks,
                           safes=safes,
                           compartments=compartments,
                           switches=switches,
                           switchports=switchports,
                           form=form)


@bp.route('/reindex', methods=['GET', 'POST'])
@login_required
def reindex():
    from app import search
    search.delete_index()
    search.create_index()

    return render_template('search.html', reindex=_("Reindexed"))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    print("user: %s" % (user.username))
    services = Service.query.all()

    return render_template('user.html', user=user,
                           services=services, title=_("User"))


@bp.route('/user/list')
@login_required
def user_list():
    page = request.args.get('page', 1, type=int)
    all = request.args.get('all', "no")
    if all != "yes":
        users = User.query.filter(User.active != "inactive").order_by(User.username).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    else:
        users = User.query.order_by(User.username).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    services = Service.query.all()

    next_url = url_for(
        'main.user_list', page=users.next_num) if users.has_next else None
    prev_url = url_for(
        'main.user_list', page=users.prev_num) if users.has_prev else None
    return render_template('users.html', users=users.items, services=services,
                           next_url=next_url, prev_url=prev_url,
                           title=_("User List"))


@bp.route('/service/add', methods=['GET', 'POST'])
@login_required
def service_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = ServiceForm()

    if form.validate_on_submit():
        service = Service(name=form.name.data, color=form.color.data)
        for u in form.users.data:
            user = User.query.filter_by(id=u).first()
            print("Adding: User: %s to: %s" % (user.username, service.name))
            service.users.append(user)
        service.manager = User.query.filter_by(id=form.manager.data).first()

        db.session.add(service)
        db.session.commit()
        audit.auditlog_new_post(
            'service', original_data=service.to_dict(), record_name=service.name)
        flash(_('Service have been saved.'))
        return redirect(url_for('main.service_list'))

    else:
        return render_template('service.html', form=form,
                               title=_("Add Service"))


@bp.route('/service/edit', methods=['GET', 'POST'])
@login_required
def service_edit():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    servicename = request.args.get('name')
    service = Service.query.filter_by(name=servicename).first()
    original_data = service.to_dict()
    if service is None:
        render_template('service.html', title=_('Service is not defined'))

    form = ServiceForm(formdata=request.form, obj=service)

    if request.method == 'POST' and form.validate_on_submit():
        # TODO remove not selected users ...
        service.users = []
        for u in form.users.data:
            user = User.query.filter_by(id=u).first()
            print("Adding: User: %s to: %s" % (user.username, service.name))
            service.users.append(user)
        service.manager = User.query.filter_by(id=form.manager.data).first()
        service.name = form.name.data
        service.color = form.color.data

        db.session.commit()
        audit.auditlog_update_post('service', original_data=original_data,
                                   updated_data=service.to_dict(), record_name=service.name)

        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.service_list'))

    else:

        pre_selected_users = [(su.id) for su in service.users]
        form = ServiceForm(users=pre_selected_users)
        form.manager.data = service.manager_id
        form.name.data = service.name
        form.color.data = service.color
        return render_template('service.html', title=_('Edit Service'),
                               form=form)


@bp.route('/service/list/', methods=['GET', 'POST'])
@login_required
def service_list():
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.updated.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.service_list',
                       page=services.next_num) if services.has_next else None
    prev_url = url_for('main.service_list',
                       page=services.prev_num) if services.has_prev else None
    return render_template('services.html', services=services.items,
                           next_url=next_url, prev_url=prev_url,
                           title=_("List Service"))


@bp.route('/service/<servicename>', methods=['GET'])
@login_required
def service_get(servicename):
    service = Service.query.filter_by(name=servicename).first_or_404()
    print("service: %s" % (service.name))

    return render_template('service.html', service=service, title=_('Service'))


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
# todo audit + rewrite
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/location/add', methods=['GET', 'POST'])
@login_required
def location_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = LocationForm()

    if form.validate_on_submit():
        location = Location()
        location.place = form.place.data
        location.area = form.area.data
        location.facillity = form.facillity.data
        location.position = form.position.data
        location.type = form.type.data
        db.session.add(location)
        db.session.commit()
        audit.auditlog_new_post(
            'location', original_data=location.to_dict(), record_name=location.longName())
        flash(_('Location have been saved.'))
        return redirect(url_for('main.location_list'))

    else:
        return render_template('location.html', form=form,
                               title=_("Add Location"))


@bp.route('/location/edit', methods=['GET', 'POST'])
@login_required
def location_edit():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    locationid = request.args.get('location')
    location = Location.query.filter_by(id=locationid).first()
    original_data = location.to_dict()
    if location is None:
        render_template('location.html', title=_('Location is not defined'))

    form = LocationForm(formdata=request.form, obj=location)

    if request.method == 'POST' and form.validate_on_submit():
        location.place = form.place.data
        location.area = form.area.data
        location.facillity = form.facillity.data
        location.position = form.position.data
        location.type = form.type.data

        db.session.commit()
        audit.auditlog_update_post('location', original_data=original_data,
                                   updated_data=location.to_dict(), record_name=location.longName())
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.location_list'))

    else:
        return render_template('location.html', title=_('Edit Location'),
                               form=form)


@bp.route('/location/list/', methods=['GET', 'POST'])
@login_required
def location_list():
    page = request.args.get('page', 1, type=int)
    locations = Location.query.order_by(Location.area.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.location_list',
                       page=locations.next_num) if locations.has_next else None
    prev_url = url_for('main.location_list',
                       page=locations.prev_num) if locations.has_prev else None
    return render_template('location.html', locations=locations.items,
                           next_url=next_url, prev_url=prev_url,
                           title=_('List Location'))


@bp.route('/updates/list/', methods=['GET'])
@login_required
def updates_list():
    page = request.args.get('page', 1, type=int)
    hsm_ped_updates = HsmPedUpdates.query.order_by(HsmPedUpdates.id).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for(
        'main.updates_list', page=hsm_ped_updates.next_num) if hsm_ped_updates.has_next else None
    prev_url = url_for(
        'main.updates_list', page=hsm_ped_updates.prev_num) if hsm_ped_updates.has_prev else None
    return render_template('updates.html', hsmpedupdates=hsm_ped_updates.items,
                           next_url=next_url, prev_url=prev_url,
                           title=_('HSM Update'))


@bp.route('/logs/list/', methods=['GET', 'POST'])
@login_required
def logs_list():
    page = request.args.get('page', 1, type=int)
    module = request.args.get('module')
    module_id = request.args.get('module_id', type=int)
    logs_for_user = request.args.get('user_id', type=int)

    if logs_for_user is not None:
        logs = Audit.query.filter_by(user_id=logs_for_user).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    elif module is not None and module_id is not None:
        logs = Audit.query.filter_by(module=module, module_id=module_id).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    elif module is not None:
        logs = Audit.query.filter_by(module=module).paginate(
            papage=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    else:
        logs = Audit.query.order_by(Audit.timestamp.desc()).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for(
        'main.logs_list', page=logs.next_num) if logs.has_next else None
    prev_url = url_for(
        'main.logs_list', page=logs.prev_num) if logs.has_prev else None
    return render_template('logs.html', logs=logs.items,
                           next_url=next_url, prev_url=prev_url,
                           title=_('Logs'))
