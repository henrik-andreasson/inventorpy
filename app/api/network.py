from app.api import bp
from flask import jsonify, current_app
from app.modules.network.models import Network
from app.models import User
from flask import url_for
from app import db
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/network/add', methods=['POST'])
@token_auth.login_required
def create_network():
    data = request.get_json() or {}
    for field in ['name', 'network', 'netmask', 'gateway', 'location_id', 'service_id']:
        if field not in data:
            return bad_request('must include %s fields' % field)

    network = Network()
    network.from_dict(data)

    db.session.add(network)
    db.session.commit()
    response = jsonify(network.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_network', id=network.id)
    return response


@bp.route('/networklist', methods=['GET'])
@token_auth.login_required
def get_networklist():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Network.to_collection_dict(Network.query, page, per_page, 'api.get_network')
    return jsonify(data)


@bp.route('/network/<int:id>', methods=['GET'])
@token_auth.login_required
def get_network(id):
    return jsonify(Network.query.get_or_404(id).to_dict())


@bp.route('/network/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_network(id):
    network = Network.query.get_or_404(id)
    data = request.get_json() or {}
    network.from_dict(data, new_network=False)
    db.session.commit()
    return jsonify(network.to_dict())


@bp.route('/network/adduser', methods=['POST'])
def add_user_to_network():

    data = request.get_json() or {}
    if 'network' not in data or 'username' not in data:
        return bad_request('must include network(name) and username fields')

    network = Network.query.filter_by(name=data['network']).first()
    user = User.query.filter_by(username=data['username']).first()

    network.users.append(user)
    db.session.commit()
    response = jsonify(network.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_network', id=network.id)
    return response
