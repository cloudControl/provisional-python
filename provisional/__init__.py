import os
import sys
import logging
import functools
import errno
from flask import Flask, request, Response
import json

app = Flask(__name__)

logger = logging.getLogger(__name__)


class ProvisionalError(Exception):
    def __init__(self, code, message):
        self._code = code
        self._message = message


class InternalServerError(ProvisionalError):
    def __init__(self):
        super(InternalServerError, self).__init__(500, 'Internal Server Error')


class BadRequestError(ProvisionalError):
    def __init__(self):
        super(BadRequestError, self).__init__(400, 'Bad Request')


class NotFoundError(ProvisionalError):
    def __init__(self):
        super(NotFoundError, self).__init__(404, 'Not found')


class ProviderError(ProvisionalError):
    def __init__(self, message):
        super(ProviderError, self).__init__(503, json.dumps({'message': str(message)}))


class Provisional():
    def read(self, resource_id):
        raise NotFoundError()

    def create(self, data):
        raise NotFoundError()

    def update(self, resource_id, data):
        raise NotFoundError()

    def delete(self, resource_id):
        raise NotFoundError()

    def health_check(self):
        return True


def handle_exceptions(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)

        except ProvisionalError as e:
            return e._message, e._code

        except Exception as e:
            logger.exception('{} {}'.format(type(e), str(e)))
            pe = InternalServerError()
            return pe._message, pe._code

    return wrapper


def check_auth(credentials, username, password):
    credentials_id = credentials['id']
    credentials_password = credentials['api']['password']
    if credentials_id == username and \
            credentials_password == password:
        return True
    return False


@app.before_request
def before():
    if app.credentials is None:
        sys.stderr.write("Credentials which were loaded before "
                         "aren't there anymore. This error is quite random?!\n")
        app.abort('Internal Server Error', 500)

    auth = request.authorization
    if not auth or not \
        check_auth(credentials=app.credentials, username=auth.username,
                   password=auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials.\n', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
    return


def json_dump(obj):
    try:
        return json.dumps(obj)
    except TypeError as e:
        sys.stderr.write('Error while serialization of {0}: {1}\n'
                         .format(str(obj), str(e)))
        return json.dumps({})


@app.route('/', methods=['GET'])
def index():
    return 'Ok', 200


@app.route('/health-check', methods=['GET'])
@handle_exceptions
def health_check():
    health_check_value = app.provisional.health_check()
    if health_check_value is None or health_check_value is False:
        return 'Service Unavailable', 503
    return 'Ok', 200


@app.route('/cloudcontrol/resources/<resource_id>', methods=['GET'])
@handle_exceptions
def read(resource_id):
    returnValue = app.provisional.read(resource_id=resource_id)
    if returnValue is None or returnValue is False:
        raise NotFoundError()

    return json_dump(returnValue), 200


@app.route('/cloudcontrol/resources/', methods=['POST'])
@handle_exceptions
def create():
    try:
        content = json.loads(request.data)
    except TypeError:
        raise BadRequestError()

    returnValue = app.provisional.create(data=content)
    if returnValue is None or returnValue is False:
        raise InternalServerError()

    return json_dump(returnValue), 201


@app.route('/cloudcontrol/resources/<resource_id>', methods=['PUT'])
@handle_exceptions
def update(resource_id):
    try:
        content = json.loads(request.data)
    except TypeError:
        raise BadRequestError()

    returnValue = app.provisional.update(
        resource_id=resource_id,
        data=content
    )

    if returnValue is None:
        raise InternalServerError()

    if returnValue is False:
        raise NotFoundError()

    return json_dump(returnValue), 200


@app.route('/cloudcontrol/resources/<resource_id>', methods=['DELETE'])
@handle_exceptions
def delete(resource_id):
    response = app.provisional.delete(resource_id=resource_id)
    if response is None or response is False:
        raise NotFoundError()

    return 'Ok', 204


def load_credentials():
    try:
        app_name = os.environ['DEP_NAME'].split('/')[0]
    except KeyError as ke:
        # not on cloudcontrol?
        sys.stderr.write("It seems that this application isn't running on "
                         "cloudControl PaaS, is it? Environment "
                         "KeyError: {0}. ERR:35\n".format(ke.message))
        sys.exit(errno.EDEADLK)

    credentials_file = 'cloudcontrol-addon-manifest.'\
        '{0}.json'.format(app_name)
    if os.path.isfile(credentials_file):
        try:
            with open(credentials_file, 'r') as contents:
                credentials = json.load(contents)
                return credentials
        except ValueError as ve:
            sys.stderr.write('JSON Error: {0}. ERR:42\n'.format(ve))
            sys.exit(errno.ENOMSG)
        except Exception as e:
            sys.stderr.write('Unexpected Error: Exception: {0}. ERR:1\n'.format(e))
            sys.exit(errno.EPERM)
    else:
        sys.stderr.write('Credentials file {0} does not '
                         'exists. ERR:2\n'.format(credentials_file))
        sys.exit(errno.ENOENT)


def load_provisional(module_name, class_name):
    '''
        dynamic class loading
    '''
    try:
        mod = __import__(module_name)
        components = module_name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

        if hasattr(mod, class_name):
            instance = getattr(mod, class_name)()
            return instance
        else:
            sys.stderr.write('Could not load class {0} from '
                             'module {1}.\nIs this class really present?\n'
                             'Using default provisional class.\n')
    except Exception as e:
        sys.stderr.write('Could not load class {0} from '
                         'module {1} ({2}).\nUsing default provisional class.\n'
                         .format(class_name, module_name, str(e)))

    return Provisional()


def load_config():
    mod = os.getenv('PROVISIONAL_MODULE', '')
    if mod:
        fnqma = mod.split('.')
        module_name = '.'.join(fnqma[:-1])
        class_name = fnqma[-1]
        app.provisional = load_provisional(module_name, class_name)
        app.credentials = load_credentials()
    else:
        raise Exception("Please define the provisional-module as environment 'PROVISIONAL_MODULE'")

try:
    load_config()
except:
    pass
