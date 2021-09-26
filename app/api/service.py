from app.api import bp
from flask import jsonify
from app.models import User, Service
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
# from flask import g, abort
from app.api.auth import token_auth


@bp.route('/service', methods=['POST'])
@token_auth.login_required
def create_service():
    data = request.get_json() or {}
    if 'name' not in data or 'color' not in data:
        return bad_request('must include name and color fields')

    check_service = Service.query.filter_by(name=data['name']).first()
    if check_service is not None:
        return bad_request('Service already exist with id: %s' % check_service.id)

    service = Service()
    service.from_dict(data, new_service=True)

    db.session.add(service)
    db.session.commit()
    audit.auditlog_new_post('service', original_data=service.to_dict(), record_name=service.name)

    response = jsonify(service.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_service', id=service.id)
    return response


@bp.route('/servicelist', methods=['GET'])
@token_auth.login_required
def get_servicelist():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Service.to_collection_dict(Service.query, page, per_page, 'api.get_service')
    return jsonify(data)


@bp.route('/service/<name>', methods=['GET'])
@token_auth.login_required
def get_service_by_name(name):

    if name is None:
        return bad_request('must include name')

    service = Service.query.filter_by(name=name).first()
    if service is None:
        return bad_request('Service with name: %s not found' % name)

    return jsonify(service.to_dict())


@bp.route('/service/<int:id>', methods=['GET'])
@token_auth.login_required
def get_service(id):
    return jsonify(Service.query.get_or_404(id).to_dict())


@bp.route('/service/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_service(id):
    service = Service.query.get_or_404(id)
    original_data = service.to_dict()

    data = request.get_json() or {}
    service.from_dict(data, new_service=False)
    db.session.commit()
    audit.auditlog_update_post('service', original_data=original_data, updated_data=service.to_dict(), record_name=service.name)
    return jsonify(service.to_dict())


@bp.route('/service/adduser', methods=['POST'])
@token_auth.login_required
def add_user_to_service():

    data = request.get_json() or {}
    if 'service' not in data or 'username' not in data:
        return bad_request('must include service(name) and username fields')

    service = Service.query.filter_by(name=data['service']).first_or_404()
    user = User.query.filter_by(username=data['username']).first_or_404()
    original_data = service.to_dict()

    service.users.append(user)
    db.session.commit()
    audit.auditlog_update_post('service', original_data=original_data, updated_data=service.to_dict(), record_name=service.name)

    response = jsonify(service.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_service', id=service.id)
    return response


@bp.route('/service/users/<servicename>', methods=['GET'])
@token_auth.login_required
def list_service_users(servicename):

    if servicename is None:
        return bad_request('must include servicename')

    service = Service.query.filter_by(name=servicename).first()
    if service is None:
        return bad_request('Service with name: %s not found' % service)

    return jsonify(service.get_users())


@bp.route('/service/users/<servicename>', methods=['POST'])
@token_auth.login_required
def set_service_users(servicename):

    if servicename is None:
        return bad_request('must include servicename')

    service = Service.query.filter_by(name=servicename).first()
    if service is None:
        return bad_request('Service with name: %s not found' % service)

    data = request.get_json() or {}
    if 'users' not in data:
        return bad_request('must include username fields')

    service.set_users(data['users'])

    return jsonify(service.get_users())


@bp.route('/service/manager/<servicename>', methods=['POST'])
@token_auth.login_required
def set_mgr_of_service(servicename):

    data = request.get_json() or {}
    if 'username' not in data:
        return bad_request('must include an username field')

    service = Service.query.filter_by(name=servicename).first_or_404()
    user = User.query.filter_by(username=data['username']).first_or_404()
    original_data = service.to_dict()

    service.manager = user
    db.session.commit()
    audit.auditlog_update_post('service', original_data=original_data, updated_data=service.to_dict(), record_name=service.name)

    response = jsonify(service.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_service', id=service.id)
    return response


@bp.route('/service/manager/<servicename>', methods=['GET'])
@token_auth.login_required
def get_mgr_of_service(servicename):

    service = Service.query.filter_by(name=servicename).first_or_404()
    response = jsonify({"manager": service.manager.username})
    response.status_code = 200
    return response
