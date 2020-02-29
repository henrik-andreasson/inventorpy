from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPin
from flask import url_for
from app import db
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

    hsmpin = HsmPin()
    hsmpin.from_dict(data)

    db.session.add(hsmpin)
    db.session.commit()
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
    data = request.get_json() or {}
    hsmpin.from_dict(data)
    db.session.commit()
    return jsonify(hsmpin.to_dict())
