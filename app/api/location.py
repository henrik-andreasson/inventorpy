from app.api import bp
from flask import jsonify
from app.models import Location
from flask import url_for
from app import db
from app.api.errors import bad_request
from flask import request
from app.api.auth import token_auth


@bp.route('/location', methods=['POST'])
@token_auth.login_required
def create_location():
    data = request.get_json() or {}
    for field in ['place', 'facillity', 'area', 'position', 'type']:
        if field not in data:
            return bad_request('must include field: %s' % field)

    location = Location()
    location.from_dict(data)

    db.session.add(location)
    db.session.commit()
    response = jsonify(location.to_dict())

    response.status_code = 201
    response.headers['Location'] = url_for('api.get_location', id=location.id)
    return response


@bp.route('/locationlist', methods=['GET'])
@token_auth.login_required
def get_locationlist():

    locations = Location.query.all()

    data = {
        'items': [(item.id,) for item in locations],
    }
    return jsonify(data)


@bp.route('/location/<int:id>', methods=['GET'])
@token_auth.login_required
def get_location(id):
    return jsonify(Location.query.get_or_404(id).to_dict())


@bp.route('/location/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_location(id):
    location = Location.query.get_or_404(id)
    data = request.get_json() or {}
    location.from_dict(data, new_location=False)
    db.session.commit()
    return jsonify(location.to_dict())
