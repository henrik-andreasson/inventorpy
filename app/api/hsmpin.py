from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPin
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmpin/add', methods=['POST'])
@token_auth.login_required
def create_hsmpin():
    data = request.get_json() or {}
    for field in ['ped_id', 'compartment_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    check_hsm_pin = HsmPin.query.filter_by(ped_id=data['ped_id']).first()
    if check_hsm_pin is not None:
        return bad_request('HSM PIN already exist with id: %s' % check_hsm_pin.id)

    hsmpin = HsmPin()
    hsmpin.from_dict(data)

    db.session.add(hsmpin)
    db.session.commit()
    audit.auditlog_new_post('hsm_pin', original_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

    response = jsonify(hsmpin.to_dict())

    response.status_code = 201
    response.headers['HsmPin'] = url_for('api.get_hsmpin', id=hsmpin.id)
    return response


@bp.route('/hsmpin/list', methods=['GET'])
@token_auth.login_required
def get_hsmpinlist():

    hsmpins = HsmPin.query.all()

    data = {
        'items': [(item.id, item.keysn) for item in hsmpins],
    }
    return jsonify(data)


@bp.route('/hsmpin/<int:id>', methods=['GET'])
@token_auth.login_required
def get_hsmpin(id):
    return jsonify(HsmPin.query.get_or_404(id).to_dict())


@bp.route('/hsmpin/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_hsmpin(id):
    hsmpin = HsmPin.query.get_or_404(id)
    original_data = hsmpin.to_dict()

    data = request.get_json() or {}
    hsmpin.from_dict(data)
    db.session.commit()
    audit.auditlog_update_post('hsm_pin', original_data=original_data, updated_data=hsmpin.to_dict(), record_name=hsmpin.ped.keyno)

    return jsonify(hsmpin.to_dict())
