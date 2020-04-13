from app.api import bp
from flask import jsonify
from app.modules.rack.models import Rack
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/rack', methods=['POST'])
@token_auth.login_required
def create_rack():
    data = request.get_json() or {}
    for field in ['name', 'location_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    rack = Rack()
    rack.from_dict(data)

    db.session.add(rack)
    db.session.commit()
    audit.auditlog_new_post('rack', original_data=rack.to_dict(), record_name=rack.name)

    response = jsonify(rack.to_dict())

    response.status_code = 201
    response.headers['Rack'] = url_for('api.get_rack', id=rack.id)
    return response


@bp.route('/racklist', methods=['GET'])
@token_auth.login_required
def get_racklist():

    racks = Rack.query.all()

    data = {
        'items': [(item.id,) for item in racks],
    }
    return jsonify(data)


@bp.route('/rack/<int:id>', methods=['GET'])
@token_auth.login_required
def get_rack(id):
    return jsonify(Rack.query.get_or_404(id).to_dict())


@bp.route('/rack/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_rack(id):
    rack = Rack.query.get_or_404(id)
    original_data = rack.to_dict()

    data = request.get_json() or {}
    rack.from_dict(data, new_rack=False)
    db.session.commit()
    audit.auditlog_update_post('rack', original_data=original_data, updated_data=rack.to_dict(), record_name=rack.name)

    return jsonify(rack.to_dict())
