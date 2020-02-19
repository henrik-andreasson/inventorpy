from flask import render_template, flash, redirect, url_for, request, g, \
    current_app, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
# from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, ServiceForm, LocationForm
from app.models import User, Service, Location
from app.modules.server.models import Server
from app.modules.hsm.models import HsmDomain, HsmPed, HsmPin
from app.modules.network.models import Network
from app.main import bp
from datetime import datetime
from rocketchat_API.rocketchat import RocketChat


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    servers = Server.query.all()
    locations = Location.query.all()
    services = Service.query.all()
    hsmdomains = HsmDomain.query.all()
    hsmpeds = HsmPed.query.all()
    hsmpins = HsmPin.query.all()
    networks = Network.query.all()

    return render_template('index.html', title=_('Explore'),
                           servers=servers, locations=locations,
                           services=services, hsmdomains=hsmdomains,
                           hsmpeds=hsmpeds, hsmpins=hsmpins,
                           networks=networks)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    print("user: %s services: %s" % (user.username, user.services))

    return render_template('user.html')


@bp.route('/service/add', methods=['GET', 'POST'])
@login_required
def service_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = ServiceForm()
    form.users.choices = [(u.username, u.username)
                          for u in User.query.all()]

    if form.validate_on_submit():
        service = Service(name=form.name.data, color=form.color.data)
        for u in form.users.data:
            user = User.query.filter_by(username=u).first()
            print("Adding: User: %s to: %s" % (user.username, service.name))
            service.users.append(user)
        db.session.add(service)
        db.session.commit()
        flash(_('Service have been saved.'))
        return redirect(url_for('main.service_list'))

    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.updated.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.service_list', page=services.next_num) if services.has_next else None
    prev_url = url_for('main.service_list', page=services.prev_num) if services.has_prev else None
    return render_template('service.html', form=form, services=services.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/service/edit', methods=['GET', 'POST'])
@login_required
def service_edit():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    servicename = request.args.get('name')
    service = Service.query.filter_by(name=servicename).first()

    if service is None:
        render_template('service.html', title=_('Service is not defined'))

    form = ServiceForm(formdata=request.form, obj=service)
# TODO select the previously selected users: service.users
    form.users.choices = [(u.username, u.username)
                          for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        # TODO remove not selected users ...
        for u in form.users.data:
            user = User.query.filter_by(username=u).first()
            print("Adding: User: %s to: %s" % (user.username, service.name))
            service.users.append(user)
        service.name = form.name.data
        service.color = form.color.data

        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.service_list'))

    else:
        return render_template('service.html', title=_('Edit Service'),
                               form=form)


@bp.route('/service/list/', methods=['GET', 'POST'])
@login_required
def service_list():
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.updated.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.service_list', page=services.next_num) if services.has_next else None
    prev_url = url_for('main.service_list', page=services.prev_num) if services.has_prev else None
    return render_template('services.html', services=services.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
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
        flash(_('Location have been saved.'))
        return redirect(url_for('main.location_list'))

    page = request.args.get('page', 1, type=int)
    locations = Location.query.order_by(Location.place).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.location_list', page=locations.next_num) if locations.has_next else None
    prev_url = url_for('main.location_list', page=locations.prev_num) if locations.has_prev else None
    return render_template('location.html', form=form, locations=locations.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/location/edit', methods=['GET', 'POST'])
@login_required
def location_edit():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    locationid = request.args.get('location')
    location = Location.query.filter_by(id=locationid).first()

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
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.location_list', page=locations.next_num) if locations.has_next else None
    prev_url = url_for('main.location_list', page=locations.prev_num) if locations.has_prev else None
    return render_template('location.html', locations=locations.items,
                           next_url=next_url, prev_url=prev_url)
