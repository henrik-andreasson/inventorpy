from app.api import bp
from flask import jsonify
from app.modules.safe.models import Safe, Compartment
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/safe', methods=['POST'])
@token_auth.login_required
def create_safe():
    data = request.get_json() or {}
    for field in ['name', 'location_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    check_safe = Safe.query.filter_by(name=data['name']).first()
    if check_safe is not None:
        return bad_request('Safe already exist with id: %s' % check_safe.id)

    safe = Safe()
    safe.from_dict(data)

    db.session.add(safe)
    db.session.commit()
    audit.auditlog_new_post('safe', original_data=safe.to_dict(), record_name=safe.name)

    response = jsonify(safe.to_dict())

    response.status_code = 201
    response.headers['Safe'] = url_for('api.get_safe', id=safe.id)
    return response


@bp.route('/safelist', methods=['GET'])
@token_auth.login_required
def get_safelist():

    safes = Safe.query.all()

    data = {
        'items': [(item.id,) for item in safes],
    }
    return jsonify(data)


@bp.route('/safe/<int:id>', methods=['GET'])
@token_auth.login_required
def get_safe(id):
    return jsonify(Safe.query.get_or_404(id).to_dict())


@bp.route('/safe/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_safe(id):
    safe = Safe.query.get_or_404(id)
    original_data = safe.to_dict()

    data = request.get_json() or {}
    safe.from_dict(data, new_safe=False)
    db.session.commit()
    audit.auditlog_update_post('safe', original_data=original_data, updated_data=safe.to_dict(), record_name=safe.name)

    return jsonify(safe.to_dict())


@bp.route('/compartment', methods=['POST'])
@token_auth.login_required
def create_compartment():
    data = request.get_json() or {}
    for field in ['name', 'safe_id', 'user_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    compartment = Compartment()
    compartment.from_dict(data)

    db.session.add(compartment)
    db.session.commit()
    audit.auditlog_new_post('compartment', original_data=compartment.to_dict(), record_name=compartment.name)

    response = jsonify(compartment.to_dict())

    response.status_code = 201
    response.headers['Compartment'] = url_for('api.get_compartment', id=compartment.id)
    return response


@bp.route('/compartmentlist', methods=['GET'])
@token_auth.login_required
def get_compartmentlist():

    compartments = Compartment.query.all()

    data = {
        'items': [(item.id,) for item in compartments],
    }
    return jsonify(data)


@bp.route('/compartment/<int:id>', methods=['GET'])
@token_auth.login_required
def get_compartment(id):
    return jsonify(Compartment.query.get_or_404(id).to_dict())


@bp.route('/compartment/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_compartment(id):
    compartment = Compartment.query.get_or_404(id)
    original_data = compartment.to_dict()

    data = request.get_json() or {}
    compartment.from_dict(data, new_compartment=False)
    db.session.commit()
    audit.auditlog_update_post('compartment', original_data=original_data, updated_data=compartment.to_dict(), record_name=compartment.name)

    return jsonify(compartment.to_dict())
