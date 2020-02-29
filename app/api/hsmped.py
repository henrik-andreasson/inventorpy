from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPed
from flask import url_for
from app import db
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmped/add', methods=['POST'])
@token_auth.login_required
def create_hsmped():
    data = request.get_json() or {}
    for field in ['keyno', 'keysn', 'hsmdomain_id', 'user_id', 'compartment_id']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    hsmped = HsmPed()
    hsmped.from_dict(data)

    db.session.add(hsmped)
    db.session.commit()
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
    data = request.get_json() or {}
    hsmped.from_dict(data)
    db.session.commit()
    return jsonify(hsmped.to_dict())
