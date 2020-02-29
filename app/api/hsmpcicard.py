from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPciCard
from flask import url_for
from app import db
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmpcicard/add', methods=['POST'])
@token_auth.login_required
def create_hsmpcicard():
    data = request.get_json() or {}
    for field in ['model', 'serial', 'fbno', 'manufacturedate', 'hsmdomain_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    if 'server_id' not in data and 'compartment_id' not in data:
        return bad_request('must include server_id or compartment_id')

    hsmpcicard = HsmPciCard()

    hsmpcicard.from_dict(data)

    db.session.add(hsmpcicard)
    db.session.commit()
    response = jsonify(hsmpcicard.to_dict())

    response.status_code = 201
    response.headers['HsmPciCard'] = url_for('api.get_hsmpcicard', id=hsmpcicard.id)
    return response


@bp.route('/hsmpcicard/list', methods=['GET'])
@token_auth.login_required
def get_hsmpcicardlist():

    hsmpcicards = HsmPciCard.query.all()

    data = {
        'items': [(item.id, item.keysn) for item in hsmpcicards],
    }
    return jsonify(data)


@bp.route('/hsmpcicard/<int:id>', methods=['GET'])
@token_auth.login_required
def get_hsmpcicard(id):
    return jsonify(HsmPciCard.query.get_or_404(id).to_dict())


@bp.route('/hsmpcicard/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_hsmpcicard(id):
    hsmpcicard = HsmPciCard.query.get_or_404(id)
    data = request.get_json() or {}
    hsmpcicard.from_dict(data)
    db.session.commit()
    return jsonify(hsmpcicard.to_dict())
