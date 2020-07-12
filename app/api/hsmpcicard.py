from app.api import bp
from flask import jsonify
from app.modules.hsm.models import HsmPciCard
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/hsmpcicard/add', methods=['POST'])
@token_auth.login_required
def create_hsmpcicard():
    data = request.get_json() or {}
    hsm_pci_card = HsmPciCard.query.filter_by(serial=data['serial']).first()
    if hsm_pci_card is not None:
        msg = 'Card already exist: %s' % hsm_pci_card.id
        return bad_request(msg)

    hsmpcicard = HsmPciCard()
    status = hsmpcicard.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.add(hsmpcicard)
    db.session.commit()
    audit.auditlog_new_post('hsm_pci_card', original_data=hsmpcicard.to_dict(), record_name=hsmpcicard.name)

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
    original_data = hsmpcicard.to_dict()

    data = request.get_json() or {}
    hsmpcicard.from_dict(data)
    db.session.commit()
    audit.auditlog_update_post('hsm_pci_card', original_data=original_data, updated_data=data, record_name=hsmpcicard.name)

    return jsonify(hsmpcicard.to_dict())
