from app.api import bp
from flask import jsonify
from app.modules.server.models import Server, VirtualServer
from flask import url_for
from app import db, audit
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/server/add', methods=['POST'])
@token_auth.login_required
def create_server():
    data = request.get_json() or {}

    if 'hostname' not in data:
        return bad_request('Hostname field is mandatory')

    check_server = Server.query.filter_by(hostname=data['hostname']).first()
    if check_server is not None:
        return bad_request('Host already exist with id: %s' % check_server.id)

    server = Server()
    status = server.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.add(server)
    db.session.commit()
    audit.auditlog_new_post('server', original_data=server.to_dict(), record_name=server.hostname)

    response = jsonify(server.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_server', id=server.id)
    return response


@bp.route('/serverlist', methods=['GET'])
@token_auth.login_required
def get_serverlist():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Server.to_collection_dict(Server.query, page, per_page, 'api.get_server')
    return jsonify(data)


@bp.route('/server/<int:id>', methods=['GET'])
@token_auth.login_required
def get_server(id):
    return jsonify(Server.query.get_or_404(id).to_dict())


@bp.route('/server/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_server(id):
    server = Server.query.get_or_404(id)
    original_data = server.to_dict()

    data = request.get_json() or {}
    server.from_dict(data, new_server=False)
    db.session.commit()
    audit.auditlog_update_post('server', original_data=original_data, updated_data=server.to_dict(), record_name=server.hostname)

    return jsonify(server.to_dict())


@bp.route('/virtual_server/add', methods=['POST'])
@token_auth.login_required
def create_virtual_server():
    data = request.get_json() or {}

    if 'hostname' not in data:
        return bad_request('Hostname field is mandatory')

    check_server = VirtualServer.query.filter_by(hostname=data['hostname']).first()
    if check_server is not None:
        return bad_request('VirtualServer already exist with id: %s' % check_server.id)

    vserver = VirtualServer()
    status = vserver.from_dict(data)
    if status['success'] is False:
        return bad_request(status['msg'])

    db.session.add(vserver)
    db.session.commit()
    audit.auditlog_new_post('virtual_server', original_data=vserver.to_dict(), record_name=vserver.hostname)

    response = jsonify(vserver.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_virtual_server', id=vserver.id)
    return response


@bp.route('/virtual_server/list', methods=['GET'])
@token_auth.login_required
def get_virtual_server_list():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = VirtualServer.to_collection_dict(Server.query, page, per_page, 'api.get_virtual_server')
    return jsonify(data)


@bp.route('/virtual_server/<int:id>', methods=['GET'])
@token_auth.login_required
def get_virtual_server(id):
    return jsonify(VirtualServer.query.get_or_404(id).to_dict())


@bp.route('/virtual_server/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_virtual_server(id):
    vserver = VirtualServer.query.get_or_404(id)
    original_data = vserver.to_dict()

    data = request.get_json() or {}
    vserver.from_dict(data, new_server=False)
    db.session.commit()
    audit.auditlog_update_post('virtual_server', original_data=original_data, updated_data=vserver.to_dict(), record_name=vserver.hostname)

    return jsonify(vserver.to_dict())
