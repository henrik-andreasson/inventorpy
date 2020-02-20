from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Service, Location
from app.modules.network.models import Network
from app.modules.network.forms import NetworkForm
from app.modules.server.models import Server
from rocketchat_API.rocketchat import RocketChat
from flask_babel import _
import ipcalc


@bp.route('/network/add', methods=['GET', 'POST'])
@login_required
def network_add():
    form = NetworkForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = NetworkForm(formdata=request.form)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.id, service.name)]

    else:
        form.service.choices = [(s.id, s.name) for s in Service.query.all()]

    location_choices = []
    for l in Location.query.all():
        formatedloc = "%s-%s-%s-%s" % (l.place, l.facillity, l.area, l.position)
        print("loc: %s:%s" % (l.id, formatedloc))
        newloc = (l.id, formatedloc)
        location_choices.append(newloc)
    form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.filter_by(id=form.location.data).first()

        network = Network(name=form.name.data,
                          network=form.network.data,
                          netmask=form.netmask.data,
                          gateway=form.gateway.data,
                          location=location)
        db.session.add(network)
        db.session.commit()
        flash(_('New network is now posted!'))

        return redirect(url_for('main.index'))

    else:

        networks = Network.query.order_by(Network.id.desc()).limit(10)
        return render_template('network.html', title=_('Add Network'),
                               form=form, networks=networks)


@bp.route('/network/edit/', methods=['GET', 'POST'])
@login_required
def network_edit():

    networkid = request.args.get('network')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.network_delete', network=networkid))

    network = Network.query.get(networkid)

    form = NetworkForm(obj=network)

    if 'selected_service' in session:
        service = Service.query.filter_by(name=session['selected_service']).first()
        form.service.choices = [(service.name, service.name)]

    else:
        form.service.choices = [(s.id, s.name) for s in Service.query.all()]
 
    location_choices = []
    for l in Location.query.all():
        formatedloc = "%s-%s-%s-%s-%s" % (l.place, l.facillity, l.area, l.position, l.type)
        print("loc: %s:%s" % (l.id, formatedloc))
        newloc = (l.id, formatedloc)
        location_choices.append(newloc)
    form.location.choices = location_choices

    if network is None:
        render_template('service.html', title=_('Network is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        string_from = '%s\t%s\t%s\t@%s\n' % (network.name, network.network,
                                             network.location, network.service)
        service = Service.query.filter_by(name=form.service.data).first()
        location = Location.query.get(form.location.data)

        network.name = form.name.data
        network.network = form.network.data
        network.netmask = form.netmask.data
        network.gateway = form.gateway.data
        network.location = location
        network.service = service

        db.session.commit()
        flash(_('Your changes have been saved.'))

        if current_app.config['ROCKET_ENABLED']:
            string_to = '%s\t%s\t%s\t@%s\n' % (network.start, network.stop,
                                               network.service, network.username)
            rocket = RocketChat(current_app.config['ROCKET_USER'],
                                current_app.config['ROCKET_PASS'],
                                network_url=current_app.config['ROCKET_URL'])
            rocket.chat_post_message('edit of network from: \n%s\nto:\n%s\nby: %s' % (
                                 string_from, string_to, current_user.username),
                                 channel=current_app.config['ROCKET_CHANNEL']
                                 ).json()

        return redirect(url_for('main.index'))

    else:
        return render_template('network.html', title=_('Edit Network'),
                               form=form)


@bp.route('/network/list/', methods=['GET', 'POST'])
@login_required
def network_list():

    page = request.args.get('page', 1, type=int)

    networks = Network.query.order_by(Network.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.network_list', page=networks.next_num) \
        if networks.has_next else None
    prev_url = url_for('main.network_list', page=networks.prev_num) \
        if networks.has_prev else None

    return render_template('network.html', title=_('Network'),
                           networks=networks.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/network/delete/', methods=['GET', 'POST'])
@login_required
def network_delete():

    networkid = request.args.get('network')
    network = Network.query.get(networkid)

    if network is None:
        flash(_('Network was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Network deleted: %s\t%s\n' % (network.name, network.network)

    flash(deleted_msg)
    db.session.delete(network)
    db.session.commit()

    return redirect(url_for('main.index'))


@bp.route('/network/view/', methods=['GET', 'POST'])
@login_required
def network_view():

    networkid = request.args.get('network')
    network = Network.query.get(networkid)

    if network is None:
        flash(_('Network was not found, id not found!'))
        return redirect(url_for('main.index'))
    network = network
    networkview = []
    netstr = "%s/%s" % (network.network, network.netmask)
    for x in ipcalc.Network(netstr):
        s = Server.query.filter_by(ipaddress=str(x)).first()
        server_net_tuple = (x, s)
        networkview.append(server_net_tuple)

    return render_template('network.html', title=_('Network'),
                           networkview=networkview,
                           network=network)
