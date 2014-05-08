import functools
from werkzeug.exceptions import HTTPException
from flask import Flask, request, Response
from flask_sslify import SSLify
import json

app = Flask(__name__)
app.provisional = None  # set this to an instance of your Provisional subclass
SSLify(app)


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


@app.before_request
def before():
    addon_id, password = app.provisional.get_credentials()

    auth = request.authorization
    if auth and auth.username == addon_id and auth.password == password:
        return

    return Response(
        'login required\n', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


@app.route('/cloudcontrol/resources/', methods=['POST'])
@handle_exceptions
def create():
    result = app.provisional.create(data=request.get_json())

    return json.dumps(result), 201


@app.route('/cloudcontrol/resources/<resource_id>', methods=['PUT'])
@handle_exceptions
def update(resource_id):
    result = app.provisional.update(
        resource_id=resource_id,
        data=request.get_json()
    )

    return json.dumps(result), 200


@app.route('/cloudcontrol/resources/<resource_id>', methods=['DELETE'])
@handle_exceptions
def delete(resource_id):
    app.provisional.delete(resource_id=resource_id)

    return 'OK', 200
