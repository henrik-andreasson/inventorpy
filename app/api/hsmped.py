from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPed
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmped/add', methods=['POST'])
@token_auth.login_required
def create_hsmped():
    data = request.get_json() or {}
    for field in ['keyno', 'keysn']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    if 'user_id' not in data and 'user_name' not in data:
        return bad_request('must include field user_name or user_id')

    if 'compartment_id' not in data and 'compartment_name' not in data:
        return bad_request('must include field compartment_id or compartment_name')

    from app.modules.hsm.models import HsmDomain
    hsmdom = None
    if 'hsmdomain_id' in data:
        hsmdom = HsmDomain.query.get_or_404(name=data['hsmdomain_id'])

    elif 'hsmdomain_name' in data:
        hsmdom = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first_or_404()

    else:
        return bad_request('must include field hsmdomain_name or hsmdomain_id')

    check_hsm_ped = HsmPed.query.filter_by(keyno=data['keyno'], keysn=data['keysn'], hsmdomain_id=hsmdom.id).first()
    if check_hsm_ped is not None:
        return bad_request('HSM PED already exist with id: %s' % check_hsm_ped.id)

    hsmped = HsmPed()
    status = hsmped.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.add(hsmped)
    db.session.commit()
    audit.auditlog_new_post('hsm_ped', original_data=hsmped.to_dict(), record_name=hsmped.keyno)
    response = jsonify(hsmped.to_dict())

    response.status_code = 201
    response.headers['HsmPed'] = url_for('api.get_hsmped', id=hsmped.id)
    return response


@bp.route('/hsmped/list', methods=['GET'])
@token_auth.login_required
def get_hsmpedlist():

    hsmpeds = HsmPed.query.all()

    data = {
        'items': [(item.id, item.keysn) for item in hsmpeds],
    }
    return jsonify(data)


@bp.route('/hsmped/<int:id>', methods=['GET'])
@token_auth.login_required
def get_hsmped(id):
    return jsonify(HsmPed.query.get_or_404(id).to_dict())


@bp.route('/hsmped/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_hsmped(id):
    hsmped = HsmPed.query.get_or_404(id)
    original_data = hsmped.to_dict()
    data = request.get_json() or {}
    hsmped.from_dict(data)
    db.session.commit()
    audit.auditlog_update_post('hsm_ped', original_data=original_data, updated_data=hsmped.to_dict(), record_name=hsmped.keyno)

    return jsonify(hsmped.to_dict())


@bp.route('/hsmped', methods=['POST'])
@token_auth.login_required
def get_hsmped_by_hsmdomain_snr():
    data = request.get_json() or {}
    if 'keysn' not in data:
        return bad_request('must include field: %s' % 'keysn')

    from app.modules.hsm.models import HsmDomain
    hsmdom = None
    if 'hsmdomain_id' in data:
        hsmdom = HsmDomain.query.get_or_404(name=data['hsmdomain_id'])

    elif 'hsmdomain_name' in data:
        hsmdom = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first_or_404()

    else:
        return bad_request('must include field hsmdomain_name or hsmdomain_id')

    hsm_ped = HsmPed.query.filter_by(keysn=data['keysn'], hsmdomain_id=hsmdom.id).first()
    if hsm_ped is None:
        return bad_request(f'HSM PED was not found hsm dom: {hsmdom.name} keysn: {data["keysn"]}')

    return jsonify(hsm_ped.to_dict())


@bp.route('/hsmped/delete', methods=['POST'])
@token_auth.login_required
def delete_hsmped_by_hsmdomain_snr():
    data = request.get_json() or {}
    if 'keysn' not in data:
        return bad_request('must include field: %s' % 'keysn')

    from app.modules.hsm.models import HsmDomain
    hsmdom = None
    if 'hsmdomain_id' in data:
        hsmdom = HsmDomain.query.get_or_404(name=data['hsmdomain_id'])

    elif 'hsmdomain_name' in data:
        hsmdom = HsmDomain.query.filter_by(name=data['hsmdomain_name']).first_or_404()

    else:
        return bad_request('must include field hsmdomain_name or hsmdomain_id')

    hsm_ped = HsmPed.query.filter_by(keysn=data['keysn'], hsmdomain_id=hsmdom.id).first()
    if hsm_ped is None:
        return bad_request(f'HSM PED was not found hsm dom: {hsmdom.name} keysn: {data["keysn"]}')

    db.session.delete(hsm_ped)
    db.session.commit()

    return jsonify(hsm_ped.to_dict())
