from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service, Location
from app.modules.network.models import Network
from app.modules.network.forms import NetworkForm
from app.modules.server.models import Server
from flask_babel import _
import ipcalc


@bp.route('/network/add', methods=['GET', 'POST'])
@login_required
def network_add():
    form = NetworkForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = NetworkForm(formdata=request.form)

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.filter_by(id=form.location.data).first()

        network = Network(name=form.name.data,
                          network=form.network.data,
                          netmask=form.netmask.data,
                          gateway=form.gateway.data,
                          vlan=form.vlan.data,
                          location=location)
        network.environment = form.environment.data

        db.session.add(network)

        db.session.commit()
        audit.auditlog_new_post('network', original_data=network.to_dict(), record_name=network.name)
        flash(_('New network is now posted!'))

        return redirect(url_for('main.index'))

    else:
        return render_template('network.html', title=_('Add Network'),
                               form=form)


@bp.route('/network/edit/', methods=['GET', 'POST'])
@login_required
def network_edit():

    networkid = request.args.get('network')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.network_delete', network=networkid))

    network = Network.query.get(networkid)
    original_data = network.to_dict()

    form = NetworkForm(obj=network)

    if network is None:
        render_template('service.html', title=_('Network is not defined'))

    if request.method == 'POST' and form.validate_on_submit():

        network.name = form.name.data
        network.network = form.network.data
        network.netmask = form.netmask.data
        network.gateway = form.gateway.data
        network.vlan = form.vlan.data
        network.location_id = form.location.data
        network.service_id = form.service.data

        db.session.commit()
        audit.auditlog_update_post('network', original_data=original_data, updated_data=network.to_dict(), record_name=network.name)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:

        form.location.data = network.location_id
        form.service.data = network.service_id
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
    audit.auditlog_delete_post('network', data=network.to_dict(), record_name=network.name)
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
