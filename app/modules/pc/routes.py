from flask import render_template, flash, redirect, url_for, request, \
    current_app, session
from flask_login import login_required
from app import db, audit
from app.main import bp
from app.models import Service, Location
from app.modules.pc.models import Pc
from app.modules.rack.models import Rack
from app.modules.pc.forms import PcForm, FilterPcListForm
from app.modules.network.models import Network
from flask_babel import _
from sqlalchemy import desc, asc


@bp.route('/pc/add', methods=['GET', 'POST'])
@login_required
def pc_add():
    form = PcForm()
    if 'cancel' in request.form:
        return redirect(request.referrer)

    form = PcForm(formdata=request.form)

    if request.method == 'POST' and form.validate_on_submit():
        service = Service.query.get(form.service.data)

        pc_checker = Pc.query.filter_by(
            serial=form.serial.data).first()
        if pc_checker is not None:
            flash(
                _(f'Pc {pc_checker.serial} is already registered, enter a different serial!'))
            return render_template('pc.html', title=_('Add PC'),
                                   form=form)

        if service is None:
            flash('Service is required')
            return redirect(request.referrer)

        pc = Pc(
                        name=form.name.data,
                        status=form.status.data,
                        network_id=form.network.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        hd=form.hd.data,
                        os_name=form.os_name.data,
                        os_version=form.os_version.data,
                        serial=form.serial.data,
                        model=form.model.data,
                        manufacturer=form.manufacturer.data,
                        comment=form.comment.data,
                        support_start=form.support_start.data,
                        support_end=form.support_end.data,
                        environment=form.environment.data,

                        )

        pc.service = service
        db.session.add(pc)
        db.session.commit()
        audit.auditlog_new_post(
            'pc', original_data=pc.to_dict(), record_name=pc.serial)
        flash(_('New pc is now posted!'))

        return redirect(url_for('main.index'))

    else:

        net_id = request.args.get('net')
        if net_id:
            form.network.default = net_id

        form.process()
        return render_template('pc.html', title=_('Add Pc'),
                               form=form)


@bp.route('/pc/edit/', methods=['GET', 'POST'])
@login_required
def pc_edit():

    pcid = request.args.get('pc')

    if 'cancel' in request.form:
        return redirect(request.referrer)
    if 'delete' in request.form:
        return redirect(url_for('main.pc_delete', pc=pcid))
    if 'copy' in request.form:
        return redirect(url_for('main.pc_copy', copy_from_pc=pcid))
    if 'logs' in request.form:
        return redirect(url_for('main.logs_list', module='pc', module_id=pcid))
    if 'switchport_list' in request.form:
        return redirect(url_for('main.switch_port_list', pcid=pcid))
    if 'switchport_add' in request.form:
        return redirect(url_for('main.switch_port_add', pcid=pcid))
    if 'qrcode' in request.form:
        return redirect(url_for('main.pc_qr', id=pcid))

# TODO: fix the link where these are going
    pc = Pc.query.get(pcid)
    original_data = pc.to_dict()

    if pc is None:
        render_template('pc.html', title=_('Pc is not defined'))

    form = PcForm(formdata=request.form, obj=pc)

    if request.method == 'POST' and form.validate_on_submit():

        pc.name = form.name.data
        pc.status = form.status.data
        pc.network_id = form.network.data
        pc.memory = form.memory.data
        pc.cpu = form.cpu.data
        pc.hd = form.hd.data
        pc.serial = form.serial.data
        pc.os_name = form.os_name.data
        pc.os_version = form.os_version.data
        pc.model = form.model.data
        pc.manufacturer = form.manufacturer.data
        pc.service_id = form.service.data
        pc.comment = form.comment.data
        pc.support_start = form.support_start.data
        pc.support_end = form.support_end.data
        pc.environment = form.environment.data

        db.session.commit()
        audit.auditlog_update_post('pc', original_data=original_data,
                                   updated_data=pc.to_dict(), record_name=pc.id)
        flash(_('Your changes have been saved.'))

        return redirect(url_for('main.index'))

    else:
        form.network.data = pc.network_id
        form.service.data = pc.service_id
#        from app.modules.switch.models import SwitchPort
 #       switchports = SwitchPort.query.filter_by(pc_id=pc.id)

        return render_template('pc.html', title=_('Edit PC'),
                               form=form, pc=pc
        )


@bp.route('/pc/copy/', methods=['GET', 'POST'])
@login_required
def pc_copy():

    pcid = request.args.get('copy_from_pc')

    if 'cancel' in request.form:
        return redirect(request.referrer)

    copy_from_pc = Pc.query.get(pcid)

    form = PcForm(obj=copy_from_pc)
    form.service.data = copy_from_pc.service_id

    if 'selected_service' in session:
        service = Service.query.filter_by(
            name=session['selected_service']).first()
        form.service.choices = [(service.id, service.name)]

    else:
        form.service.choices = [(s.id, s.name) for s in Service.query.all()]

    if copy_from_pc is None:
        render_template('service.html', title=_('Pc is not defined'))

    if request.method == 'POST' and form.validate_on_submit():
        pc = Pc(
                        name=form.name.data,
                        status=form.status.data,
                        network_id=form.network.data,
                        memory=form.memory.data,
                        cpu=form.cpu.data,
                        hd=form.hd.data,
                        os_name=form.os_name.data,
                        os_version=form.os_version.data,
                        serial=form.serial.data,
                        model=form.model.data,
                        manufacturer=form.manufacturer.data,
                        comment=form.comment.data,
                        support_start=form.support_start.data,
                        support_end=form.support_end.data,
                        environment=form.environment.data,

                        )
        service = Service.query.get(form.service.data)
        pc.service = service
        db.session.add(pc)

        db.session.commit()
        audit.auditlog_new_post(
            'pc', original_data=pc.to_dict(), record_name=pc.id)
        flash(
            _(f'Created new pc: {pc.id} with vales based on {copy_from_pc.id}'))
        return redirect(url_for('main.index'))

    else:
        return render_template('pc.html', title=_('Copy Pc'),
                               form=form)


@bp.route('/pc/list/', methods=['GET', 'POST'])
@login_required
def pc_list():

    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'serial')
    order = request.args.get('order', 'asc')
    pc_vars = list(vars(Pc).keys())

    if sort not in pc_vars:
        flash(_('No such varibale to sort by %s' % sort))
        return redirect(url_for('main.index'))

    if order not in ['asc', 'desc']:
        flash(_('Bad order to sort by'))
        return redirect(url_for('main.index'))

    sortstr = "{}(Pc.{})".format(order, sort)
    form = FilterPcListForm()

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
        input_search_query.append('(Pc.service_id == service.id)')
    if environment is not None and environment != "all":
        print("env: {}".format(environment))
        input_search_query.append('(Pc.environment == environment)')

    if len(input_search_query) < 1:
        pcs = Pc.query.order_by(eval(sortstr)).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    else:
        query = " & ".join(input_search_query)
        print("query: {}".format(query))
        pcs = Pc.query.filter(eval(query)).order_by(eval(sortstr)).paginate(
            page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('main.pc_list', page=pcs.next_num) \
        if pcs.has_next else None
    prev_url = url_for('main.pc_list', page=pcs.prev_num) \
        if pcs.has_prev else None

    return render_template('pc.html', title=_('Pc'),
                           pcs=pcs.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/pc/delete/', methods=['GET', 'POST'])
@login_required
def pc_delete():

    pcid = request.args.get('pc')
    pc = Pc.query.get(pcid)

    if pc is None:
        flash(_('PC was not deleted, id not found!'))
        return redirect(url_for('main.index'))

    deleted_msg = 'PC deleted: %s\n' % (pc.serial)
    flash(deleted_msg)
    db.session.delete(pc)
    db.session.commit()
    audit.auditlog_delete_post(
        'pc', data=pc.to_dict(), record_name=pc.serial)

    return redirect(url_for('main.index'))



@bp.route('/pc/qr/<int:id>', methods=['GET'])
@login_required
def pc_qr(id):

    pc = Pc.query.get(id)

    if pc is None:
        flash(_('PC was found, id not found!'))
        return redirect(url_for('main.index'))

    qr_data = url_for("main.pc_edit", pc=pc.id, _external=True)
    return render_template('pc_qr.html', title=_('QR PC'),
                           pc=pc, qr_data=qr_data)
