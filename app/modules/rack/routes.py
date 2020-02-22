from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Service, Location, User
from app.modules.rack.models import Rack
from app.modules.rack.forms import RackForm
from rocketchat_API.rocketchat import RocketChat
from flask_babel import _


@bp.route('/rack/add', methods=['GET', 'POST'])
@login_required
def rack_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = RackForm(formdata=request.form)

    location_choices = []
    for l in Location.query.all():
        newloc = (l.id, l.longName())
        location_choices.append(newloc)
    form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():

        location = Location.query.get(form.location.data)
        rack = Rack(name=form.name.data)
        rack.location = location
        db.session.add(rack)
        db.session.commit()
        flash(_('New Rack is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('rack.html', title=_('Rack'),
                               form=form)


@bp.route('/rack/edit/', methods=['GET', 'POST'])
@login_required
def rack_edit():

    rackid = request.args.get('rack')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.rack_delete', rack=rackid))

    rack = Rack.query.get(rackid)
    form = RackForm(obj=rack)

    if rack is None:
        flash(_('Rack not found'))
        return redirect(request.referrer)

    location_choices = []
    for l in Location.query.all():
        newloc = (l.id, l.longName())
        location_choices.append(newloc)
    form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.get(form.location.data)

        rack.name = form.name.data
        rack.location = location
        db.session.commit()
        flash(_('Your changes to the rack have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('rack.html', title=_('Edit Rack'),
                               form=form)


@bp.route('/rack/list/', methods=['GET', 'POST'])
@login_required
def rack_list():

    page = request.args.get('page', 1, type=int)

    racks = Rack.query.order_by(Rack.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.rack_list', page=racks.next_num) \
        if racks.has_next else None
    prev_url = url_for('main.rack_list', page=racks.prev_num) \
        if racks.has_prev else None

    return render_template('rack.html', title=_('Rack'),
                           racks=racks.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/rack/delete/', methods=['GET', 'POST'])
@login_required
def rack_delete():

    rackid = request.args.get('rack')
    rack = Rack.query.get(rackid)

    if rack is None:
        flash(_('Rack was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Rack deleted: %s %s' % (rack.name,
                                           rack.location.longName())
    db.session.delete(rack)
    db.session.commit()
    flash(deleted_msg)

    return redirect(url_for('main.index'))
