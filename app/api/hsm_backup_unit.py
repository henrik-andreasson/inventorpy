from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmBackupUnit
from app.modules.safe.models import Safe
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsm_backup_unit/add', methods=['POST'])
@token_auth.login_required
def create_hsm_backup_unit():
    data = request.get_json() or {}

    for field in ['name', 'serial', 'model', 'manufacturedate', 'fbno']:
        if field not in data:
            return bad_request(f'must include field: {field}')

    safe = None
    if 'safe_name' in data:
        safe = Safe.query.filter_by(name=data['safe_name']).first()
    elif 'safe_id' in data:
        safe = Safe.query.get(data['safe_id'])
    else:
        return bad_request(f'must include field: safe_id or safe_name')

    if safe is None:
        return bad_request(f'must include field: safe_id or safe_name')

    hsm_backup_unit = HsmBackupUnit.query.filter_by(serial=data['serial']).first()
    if hsm_backup_unit is not None:
        msg = 'Backup unit already exist: %s' % hsm_backup_unit.id
        return bad_request(msg)

    hsm_backup_unit = HsmBackupUnit()
    status = hsm_backup_unit.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.add(hsm_backup_unit)
    db.session.commit()
    audit.auditlog_new_post('hsm_backup_unit', original_data=hsm_backup_unit.to_dict(), record_name=hsm_backup_unit.name)

    response = jsonify(hsm_backup_unit.to_dict())

    response.status_code = 201
    response.headers['HsmBackupUnit'] = url_for('api.get_hsm_backup_unit', id=hsm_backup_unit.id)
    return response


@bp.route('/hsm_backup_unit/list', methods=['GET'])
@token_auth.login_required
def get_hsm_backup_unitlist():

    hsm_backup_units = HsmBackupUnit.query.all()

    data = {
        'items': [(item.id, item.keysn) for item in hsm_backup_units],
    }
    return jsonify(data)


@bp.route('/hsm_backup_unit/<int:id>', methods=['GET'])
@token_auth.login_required
def get_hsm_backup_unit(id):
    return jsonify(HsmBackupUnit.query.get_or_404(id).to_dict())


@bp.route('/hsm_backup_unit/<name>', methods=['GET'])
@token_auth.login_required
def get_hsm_backup_unit_by_name(name):
    return jsonify(HsmBackupUnit.query.filter_by(name=name).first_or_404().to_dict())


@bp.route('/hsm_backup_unit/update', methods=['POST'])
@token_auth.login_required
def update_hsm_backup_unit_by_name():
    data = request.get_json() or {}

    hsm_backup_unit = None
    if 'hsm_backup_unit_id' in data:
        hsm_backup_unit = HsmBackupUnit.query.get(id)
    elif 'hsm_backup_unit_name' in data:
        hsm_backup_unit = HsmBackupUnit.query.filter_by(name=data['hsm_backup_unit_name']).first()
    else:
        return bad_request(f'must include field: hsm_backup_unit_id or hsm_backup_unit_name')

    if hsm_backup_unit is None:
        return bad_request(f'could not find backupunit via the id nor name')

    safe = None
    if 'safe_name' in data:
        safe = Safe.query.filter_by(name=data['safe_name']).first()
        data['safe_id'] = safe.id
    elif 'safe_id' in data:
        safe = Safe.query.get(data['safe_id'])
        data['safe_id'] = safe.id

    original_data = hsm_backup_unit.to_dict()
    status = hsm_backup_unit.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.update(hsm_backup_unit)
    db.session.commit()
    audit.auditlog_update_post('hsm_backup_unit', original_data=original_data, updated_data=hsm_backup_unit.to_dict(), record_name=hsm_backup_unit.name)

    response = jsonify(hsm_backup_unit.to_dict())

    response.status_code = 201
    response.headers['HsmBackupUnit'] = url_for('api.get_hsm_backup_unit', id=hsm_backup_unit.id)
    return response


@bp.route('/hsm_backup_unit/delete', methods=['POST'])
@token_auth.login_required
def del_hsm_backup_unit():
    data = request.get_json() or {}

    hsm_backup_unit = None
    if 'hsm_backup_unit_id' in data:
        hsm_backup_unit = HsmBackupUnit.query.get(id)
    elif 'hsm_backup_unit_name' in data:
        hsm_backup_unit = HsmBackupUnit.query.filter_by(name=data['hsm_backup_unit_name']).first()
    else:
        return bad_request(f'must include field: hsm_backup_unit_id or hsm_backup_unit_name')

    if hsm_backup_unit is None:
        return bad_request(f'could not find backupunit via the id nor name')

    audit.auditlog_update_post('hsm_backup_unit', data=hsm_backup_unit.to_dict(), record_name=hsm_backup_unit.name)

    db.session.delete(hsm_backup_unit)
    db.session.commit()
    return jsonify(hsm_backup_unit.to_dict())
