from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPin
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth
from app.modules.safe.models import Compartment


@bp.route('/hsmpin/add', methods=['POST'])
@token_auth.login_required
def create_hsmpin():
    data = request.get_json() or {}
    if 'ped_id' not in data:
        return bad_request('must include field: ped_id')

    if 'compartment_id' in data:
        check_comp = Compartment.query.get_or_404(data['compartment_id'])
    elif 'compartment_name' in data:
        check_comp = Compartment.query.filter_by(name=data['compartment_name']).first()
    else:
        return bad_request('Compartment not found via id nor name')

    if check_comp is None:
        return bad_request('Compartment not found via id nor name')
    else:
        data['compartment_id'] = check_comp.id

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
    page = request.args.get('page', 1, type=int)
    print(f"page: {page}")
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = HsmPin.to_collection_dict(HsmPin.query, page, per_page, 'api.get_hsmpinlist')
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


@bp.route('/hsmpin', methods=['POST'])
@token_auth.login_required
def get_hsmpin_via_pedkeysn_and_hsmdom():
    data = request.get_json() or {}
    if 'ped_id' not in data:
        return bad_request('must include ped_id')

    hsm_pin = HsmPin.query.filter_by(ped_id=data['ped_id']).first()
    if hsm_pin is None:
        return bad_request(f'HSM PIN was not found ped_id: {data["ped_id"]}')

    return jsonify(hsm_pin.to_dict())


@bp.route('/hsmpin', methods=['DELETE'])
@token_auth.login_required
def del_hsmpin_via_pedkeysn_and_hsmdom():
    data = request.get_json() or {}
    if 'ped_id' not in data:
        return bad_request('must include ped_id')

    hsm_pin = HsmPin.query.filter_by(ped_id=data['ped_id']).first()
    if hsm_pin is None:
        return bad_request(f'HSM PIN was not found hsm {data["ped_id"]}')

    db.session.delete(hsm_pin)
    db.session.commit()
    return jsonify(hsm_pin.to_dict())
