import functools
from werkzeug.exceptions import HTTPException
from flask import Blueprint, request, Response
from flask_sslify import SSLify
import json


class ProvisionalBlueprint(Blueprint):
    def __init__(self):
        Blueprint.__init__(self, 'provisional', __name__)
        self.provisional = None
        SSLify(self)

blueprint = ProvisionalBlueprint()


def handle_provisional(app=None):
    def wrapped(cls):
        blueprint.provisional = cls()

        if app:
            app.register_blueprint(blueprint)

    return wrapped


class Provisional(object):
    def create(self, data):
        raise NotImplementedError()

    def update(self, resource_id, data):
        raise NotImplementedError()

    def delete(self, resource_id):
        raise NotImplementedError()

    def get_credentials(self):
        raise NotImplementedError()


def handle_exceptions(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HTTPException as e:
            return json.dumps({'message': str(e.description)}), e.code

    return wrapper


@blueprint.before_request
def check_credentials():
    addon_id, password = blueprint.provisional.get_credentials()

    auth = request.authorization
    if auth and auth.username == addon_id and auth.password == password:
        return

    return Response(
        'login required\n', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


@blueprint.route('/cloudcontrol/resources/', methods=['POST'])
@handle_exceptions
def create():
    result = blueprint.provisional.create(data=request.get_json())

    return json.dumps(result), 201


@blueprint.route('/cloudcontrol/resources/<resource_id>', methods=['PUT'])
@handle_exceptions
def update(resource_id):
    result = blueprint.provisional.update(
        resource_id=resource_id,
        data=request.get_json()
    )

    return json.dumps(result), 200


@blueprint.route('/cloudcontrol/resources/<resource_id>', methods=['DELETE'])
@handle_exceptions
def delete(resource_id):
    blueprint.provisional.delete(resource_id=resource_id)

    return 'OK', 200
