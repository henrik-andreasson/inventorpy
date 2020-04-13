from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmDomain
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmdomain/add', methods=['POST'])
@token_auth.login_required
def create_hsmdomain():
    data = request.get_json() or {}
    for field in ['name', 'service_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    hsmdomain = HsmDomain()
    hsmdomain.from_dict(data)

    db.session.add(hsmdomain)
    db.session.commit()
    audit.auditlog_new_post('hsm_domain', original_data=hsmdomain.to_dict(), record_name=hsmdomain.name)

    response = jsonify(hsmdomain.to_dict())

    response.status_code = 201
    response.headers['HsmDomain'] = url_for('api.get_hsmdomain', id=hsmdomain.id)
    return response


@bp.route('/hsmdomain/list', methods=['GET'])
@token_auth.login_required
def get_hsmdomainlist():

    hsmdomains = HsmDomain.query.all()

    data = {
        'items': [(item.id,) for item in hsmdomains],
    }
    return jsonify(data)


@bp.route('/hsmdomain/<int:id>', methods=['GET'])
@token_auth.login_required
def get_hsmdomain(id):
    return jsonify(HsmDomain.query.get_or_404(id).to_dict())


@bp.route('/hsmdomain/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_hsmdomain(id):
    hsmdomain = HsmDomain.query.get_or_404(id)
    original_data = hsmdomain.to_dict()
    data = request.get_json() or {}
    hsmdomain.from_dict(data, new_hsmdomain=False)
    db.session.commit()
    audit.auditlog_update_post('hsm_domain', original_data=original_data, updated_data=data)

    return jsonify(hsmdomain.to_dict())
