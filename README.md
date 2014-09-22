# provisional-python

provisional-python is a Flask blueprint for the add-on provisioning
API and can be used by cloudControl service providers.

Detailed documentation on how to join the cloudControl Add-on Provider
Program and the business process can be found here:

https://www.cloudcontrol.com/add-on-provider-program

The PHP version can be found here:

https://github.com/cloudcontrol/provisional


## Usage

### Install provisional-python

``` sh
pip install git+git://github.com/cloudControl/provisional-python.git@VERSION
```


### Build your addon provisional class

``` python
# file: my_addon.py
from flask import Flask
from provisional import handle_provisional

app = Flask(__name__)

@handle_provisional(app)
class MyAddonProvisional(object):

    def create(self, data):
        """Create addon

        create() is called on each provisioning request. data is a
        dictionary containing the parsed request body.

        Use the provided data to provision your service.

        Finally you have to return a dictionary as below.

        Make sure "config" list all config variables as defined
        in your manifest file.
        """

        return {
            "id": "YOUR_INTERNAL_ID",
            "config": {
                "MYADDON_VAR": "VALUE"
            }
        }


    def update(self, resource_id, data):
        """Update addon

        update() gets called on each plan change and gets passed
        both the id you returned upon provisioning (YOUR_INTERNAL_ID)
        and the request data as dictionary.

        If there's only one plan for your addon, you don't have to
        implement update.

        The response is similar to the one from create() but without
        the id.
        """

        return {
            "config": {
                "MYADDON_VAR": "VALUE"
            }
        }

    def delete(self, resource_id):
        """ Delete addon

        Should return 'True' on sucess.
        """

        return True

    def get_credentials(self)
        """Provide addon credentials

        Is expected to return a tuple (addon_id, password) which
        is used by provisional-python to authenticate all requests.
        """

        return ('ADDON_ID', 'SECRET')
```

#### Error handling

To communicate an error, you should raise either `UnprocessableEntity`
or `ServiceUnavailable` as defined in werkzeug.exceptions:

https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/exceptions.py

### Add a Procfile

Example:

```
web: gunicorn -b 0.0.0.0:$PORT -w $(ncproc) 'myapplication:app'
```
