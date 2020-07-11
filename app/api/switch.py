from app.api import bp
from flask import jsonify
from app.modules.switch.models import Switch, SwitchPort
from app.modules.rack.models import Rack
from app.modules.network.models import Network
from app.modules.server.models import Server
from app.models import Service, Location
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/switch/add', methods=['POST'])
@token_auth.login_required
def create_switch():
    data = request.get_json() or {}
    for field in ['name', 'status']:
        if field not in data:
            return bad_request('must include %s fields' % field)

    check_switch = Switch.query.filter_by(name=data['name']).first()
    if check_switch is not None:
        return bad_request('Switch already exist with id: %s' % check_switch.id)

    switch = Switch()
    switch.from_dict(data)

    if 'service_id' in data:
        service = Service.query.get(data['service_id'])
        switch.service = service

    if 'location_id' in data:
        location = Location.query.get(data['location_id'])
        switch.location = location

    if 'rack_id' in data:
        rack = Rack.query.get(data['rack_id'])
        switch.rack = rack

    db.session.add(switch)
    db.session.commit()
    audit.auditlog_new_post('switch', original_data=switch.to_dict(), record_name=switch.name)

    response = jsonify(switch.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_switch', id=switch.id)
    return response


@bp.route('/switchlist', methods=['GET'])
@token_auth.login_required
def get_switchlist():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Switch.to_collection_dict(Switch.query, page, per_page, 'api.get_switch')
    return jsonify(data)


@bp.route('/switch/<int:id>', methods=['GET'])
@token_auth.login_required
def get_switch(id):
    return jsonify(Switch.query.get_or_404(id).to_dict())


@bp.route('/switch/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_switch(id):
    switch = Switch.query.get_or_404(id)
    original_data = switch.to_dict()

    data = request.get_json() or {}
    switch.from_dict(data, new_switch=False)
    db.session.commit()
    audit.auditlog_update_post('switch', original_data=original_data, updated_data=switch.to_dict(), record_name=switch.hostname)

    return jsonify(switch.to_dict())


@bp.route('/switch/port/add', methods=['POST'])
@token_auth.login_required
def switch_port_add():
    data = request.get_json() or {}
    for field in ['name', 'switch']:
        if field not in data:
            return bad_request('must include %s fields' % field)

    switch = Switch.query.filter_by(name=data['switch']).first()
    if switch is None:
        return bad_request('No such Switch name exist in the db')
    else:
        print("adding port to switch: {} {}".format(switch.name, switch.id))

    check_sp = SwitchPort.query.filter_by(name=data['name'], switch_id=switch.id).first()
    if check_sp is not None:
        return bad_request('SwitchPort already exist with id: %s' % check_sp.id)
    else:
        print("the port {} was not found, adding".format(data['name']))

    network = None
    server = None
    if 'network_id' in data:
        network = Network.query.get(data['network_id'])
    elif 'network_name' in data:
        network = Network.query.filter_by(name=data['network_name']).first()

    if 'server_id' in data:
        server = server.query.get(data['rack_id'])
    elif 'server_name' in data:
        server = Server.query.filter_by(name=data['rack_name'])

    switch_port = SwitchPort()
    switch_port.from_dict(data)
    switch_port.switch = switch
    switch_port.network = network
    switch_port.server = server

    db.session.add(switch_port)
    db.session.commit()
    audit.auditlog_new_post('switch', original_data=switch_port.to_dict(), record_name=switch_port.name)

    response = jsonify(switch_port.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_switch_port', id=switch_port.id)
    return response


@bp.route('/switch/port/list', methods=['GET'])
@token_auth.login_required
def get_switch_port_list():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SwitchPort.to_collection_dict(SwitchPort.query, page, per_page, 'api.get_switch_port')
    return jsonify(data)


@bp.route('/switch/port/<int:id>', methods=['GET'])
@token_auth.login_required
def get_switch_port(id):
    return jsonify(SwitchPort.query.get_or_404(id).to_dict())


@bp.route('/switch/port/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_switch_port(id):
    switch_port = SwitchPort.query.get_or_404(id)
    original_data = switch_port.to_dict()

    data = request.get_json() or {}
    switch_port.from_dict(data, new_switch=False)
    db.session.commit()
    audit.auditlog_update_post('switch', original_data=original_data, updated_data=switch_port.to_dict(), record_name=switch_port.name)

    return jsonify(switch_port.to_dict())
