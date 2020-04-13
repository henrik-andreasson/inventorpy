from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Location, User
from app.modules.safe.models import Safe, Compartment
from app.modules.safe.forms import SafeForm, CompartmentForm
from flask_babel import _


@bp.route('/safe/add', methods=['GET', 'POST'])
@login_required
def safe_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = SafeForm(formdata=request.form)

    # location_choices = []
    # for l in Location.query.all():
    #     formatedloc = "%s-%s-%s-%s" % (l.place, l.facillity, l.area, l.position)
    #     print("loc: %s:%s" % (l.id, formatedloc))
    #     newloc = (l.id, formatedloc)
    #     location_choices.append(newloc)
    # form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():

        location = Location.query.get(form.location.data)
        safe = Safe(name=form.name.data)
        safe.location = location
        db.session.add(safe)
        db.session.commit()
        audit.auditlog_new_post('safe', original_data=safe.to_dict(), record_name=safe.name)

        flash(_('New Safe is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('safe.html', title=_('Safe'),
                               form=form)


@bp.route('/safe/edit/', methods=['GET', 'POST'])
@login_required
def safe_edit():

    safeid = request.args.get('safe')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.safe_delete', safe=safeid))

    safe = Safe.query.get(safeid)
    form = SafeForm(obj=safe)
    original_data = safe.to_dict()

    if safe is None:
        flash(_('Safe not found'))
        return redirect(request.referrer)
    #
    # location_choices = []
    # for l in Location.query.all():
    #     newloc = (l.id, l.longName())
    #     location_choices.append(newloc)
    # form.location.choices = location_choices

    if request.method == 'POST' and form.validate_on_submit():
        location = Location.query.get(form.location.data)

        safe.name = form.name.data
        safe.location = location
        db.session.commit()
        audit.auditlog_update_post('safe', original_data=original_data, updated_data=safe.to_dict(), record_name=safe.name)

        flash(_('Your changes to the safe have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.location.data = safe.location_id

        return render_template('safe.html', title=_('Edit Safe'),
                               form=form)


@bp.route('/safe/list/', methods=['GET', 'POST'])
@login_required
def safe_list():

    page = request.args.get('page', 1, type=int)

    safes = Safe.query.order_by(Safe.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.safe_list', page=safes.next_num) \
        if safes.has_next else None
    prev_url = url_for('main.safe_list', page=safes.prev_num) \
        if safes.has_prev else None

    return render_template('safe.html', title=_('Safe'),
                           safes=safes.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/safe/delete/', methods=['GET', 'POST'])
@login_required
def safe_delete():

    safeid = request.args.get('safe')
    safe = Safe.query.get(safeid)

    if safe is None:
        flash(_('Safe was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Safe deleted: %s %s' % (safe.name,
                                           safe.location.longName())
    db.session.delete(safe)
    db.session.commit()
    audit.auditlog_delete_post('safe', data=safe.to_dict(), record_name=safe.name)
    flash(deleted_msg)

    return redirect(url_for('main.index'))


@bp.route('/compartment/add', methods=['GET', 'POST'])
@login_required
def compartment_add():
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = CompartmentForm(formdata=request.form)

    form.safe.choices = [(s.id, s.name) for s in Safe.query.all()]
    form.user.choices = [(u.id, u.username) for u in User.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(form.user.data)
        safe = Safe.query.get(form.safe.data)
        compartment = Compartment(name=form.name.data)
        compartment.safe = safe
        compartment.user = user
        db.session.add(compartment)
        db.session.commit()
        audit.auditlog_new_post('compartment', original_data=compartment.to_dict(), record_name=compartment.name)

        flash(_('New Compartment is now posted!'))

        return redirect(url_for('main.index'))

    else:

        return render_template('safe.html', title=_('Compartment'),
                               form=form)


@bp.route('/compartment/edit/', methods=['GET', 'POST'])
@login_required
def compartment_edit():

    compartmentid = request.args.get('compartment')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.compartment_delete', compartment=compartmentid))

    compartment = Compartment.query.get(compartmentid)
    original_data = compartment.to_dict()

    form = CompartmentForm(obj=compartment)
    form.safe.choices = [(s.id, s.name) for s in Safe.query.all()]
    form.user.choices = [(u.id, u.username) for u in User.query.all()]

    if compartment is None:
        flash(_('Compartment not found'))
        return redirect(request.referrer)

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(form.user.data)
        safe = Safe.query.get(form.safe.data)
        compartment.name = form.name.data
        compartment.safe = safe
        compartment.user = user
        db.session.commit()
        audit.auditlog_update_post('compartment', original_data=original_data, updated_data=compartment.to_dict(), record_name=compartment.name)

        flash(_('Your changes to the compartment have been saved.'))

        return redirect(url_for('main.index'))

    else:
        return render_template('safe.html', title=_('Edit Compartment'),
                               form=form)


@bp.route('/compartment/list/', methods=['GET', 'POST'])
@login_required
def compartment_list():

    page = request.args.get('page', 1, type=int)

    compartments = Compartment.query.order_by(Compartment.name).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.compartment_list', page=compartments.next_num) \
        if compartments.has_next else None
    prev_url = url_for('main.compartment_list', page=compartments.prev_num) \
        if compartments.has_prev else None

    return render_template('safe.html', title=_('Compartment'),
                           compartments=compartments.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/compartment/delete/', methods=['GET', 'POST'])
@login_required
def compartment_delete():

    compartmentid = request.args.get('compartment')
    compartment = Compartment.query.get(compartmentid)

    if compartment is None:
        flash(_('Compartment was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'Compartment deleted: %s' % (compartment.name)
    db.session.delete(compartment)
    db.session.commit()
    audit.auditlog_delete_post('compartment', data=compartment.to_dict(), record_name=compartment.name)

    flash(deleted_msg)

    return redirect(url_for('main.index'))
