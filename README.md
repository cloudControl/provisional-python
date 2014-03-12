# provisional.py

CloudControl's python addon [provisional](https://github.com/cloudControl/provisional)
wrapper.

### Usage

1. Write your addon manifest.
   To get more informations about how to, have a look at cloudControl's
   [Add-on Provider Program](https://www.cloudcontrol.com/add-on-provider-program)


2. Install cloudcontrol's provisional.py

    ``` sh
    $ pip install git+git://github.com/cloudControl/provisional-python.git@master
    ```

    Or add it as git submodule to your own addon provisional project

    ``` sh
    $ git submodule add https://github.com/cloudControl/provisional-python.git provisional
    ```


3. Implement your addon provisional Class

    ``` python
    # -*- coding: utf-8 -*-
    # file: my_addon_provisional.py

    from provisional import Provisional

    class MyAddonProvisional(Provisional):
        def __init__(self):
            super(Provisional, self).__init__()

        def read(self, resource_id):
            '''
                read is disabled for this addon
            '''
            e = Exception()
            e.code = 404
            e.message = 'Not found'
            raise e

        def create(self, data):
            '''
                creation is disabled
            '''
            e = Exception()
            e.code = 404
            e.message = 'Not found'
            raise e

        def update(self, resource_id, data):
            '''
                do some business logic here
            '''
            return data

        def delete(self, resource_id):
            '''
                delete succeeded
            '''
            return True

        def health_check(self):
            return True
    ```


4. Write your Procfile

    ``` text
    web: python -m provisional my_addon_provisional.MyAddonProvisional
    ```

### Provisional Methodology Specs

#### def read(self, resource_id):

The 'read' method access the resource with the specified id.

(function is optional - raises by default Exception(404, Not Found))

* arguments
  * resource_id - the resources id - the resource to update with the concerning id

* returns Object
  * serializable object - if given - the just updated entity

* raises Exception
  * exception.message - if given - defines the message of the http response
  * exception.code - if given - defines the response code of the http response

#### def create(self, data):

The 'create' method creates the resource with specific properties.

(function is optional - raises by default Exception(404, Not Found))

* arguments
  * data - the resource to create

* returns Object
  * serializable object - if given - the resource which was just created
  * None - means something went wrong

#### def update(self, resource_id, data):

The 'update' method updates the resource with the given id.

(function is optional - raises by default Exception(404, Not Found))

* arguments
  * resource_id - the resources id - the resource to update with the concerning id
  * data

* returns Object
  * serializable object - if given - the just updated entity
  * None
    * return 'Internal Server Error', 500

* raises Exception
  * exception.message - if given - defines the message of the http response
  * exception.code - if given - defines the response code of the http response

#### def delete(self, resource_id):

The 'delete' method deletes the resource with the specified id.

(function is optional - raises by default Exception(404, Not Found))

* arguments
  * resource_id - the resources id - the resource to delete with the concerning id

* returns Boolean
  * True if success

* raises Exception
  * exception.message - if given - defines the message of the http response
  * exception.code - if given - defines the response code of the http response

#### def health_check(self):

Through the 'health_check' method you can perform some dependency checks.
which should not fail to serve the provisioning

(function is optional - returns by default True )

* returns Boolean
  * True if success

* raises Exception
  * If an execption raises the server will be HTTP 503 SERVICE UNAVAILABLE
