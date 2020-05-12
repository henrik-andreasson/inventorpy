from app.api import bp
from flask import jsonify
from app.modules.switch.models import Switch
from app.modules.rack.models import Rack
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
    for field in ['name', 'status', 'rack_id', 'location_id', 'service_id']:
        if field not in data:
            return bad_request('must include %s fields' % field)

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
    audit.auditlog_new_post('switch', original_data=switch.to_dict(), record_name=switch.hostname)

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
