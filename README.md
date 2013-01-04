# provisional.py

CloudControl's python addon provisional wrapper.

### Usage
---

1. Write your addon manifest.
   To get more informations about how to, have a look at cloudControl's [Add-on Provider Program](https://www.cloudcontrol.com/add-on-provider-program)


2. Install cloudcontrol's provisional.py

        $ pip install git+git://github.com/cloudControl/provisional-python.git@master

        Or add it as git submodule to your own addon provisional project

        $ git submodule add https://github.com/cloudControl/provisional-python.git provisional

>       *Notice: If you chose the submodule's way the README's way may vary.*


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
---

  * #### def read(self, resource_id):
>	*The 'read' method access the resource with the specified id.*
>
>	*(this function is optional - raises by default* Exception(404, Not Found) )

    * arguments
<ul>
<li>   *self - the object itself - self explanatory*</li>
<li>   *resource_id - the resources id - the resource to update with the concerning id*</li>
</ul>
    * returns Object
<ul>
<li>   *serializable object - if given - the just updated entity*</li>
</ul>
    * raises Exception
<ul>
<li>  *exception.message - if given - defines the message of the http response*</li>
<li>  *exception.code - if given - defines the response code of the http response*</li>
</ul>


  * #### def create(self, data):
>	*The 'create' method creates the resource with specific properties.*
>
>	*(this function is optional - raises by default* Exception(404, Not Found) )

    * arguments
<ul>
<li>  *self - the object itself - self explanatory*</li>
<li>  *data - the resource to create*</li>
</ul>
    * returns Object
<ul>
<li>  *serializable object - if given - the resource which was just created*</li>
<li>  *None - means something went wrong*</li>
</ul>
    * raises Exception
<ul>
<li>  *exception.message - if given - defines the message of the http response*</li>
<li>  *exception.code - if given - defines the response code of the http response*</li>
</ul>



  * #### def update(self, resource_id, data):
>	*The 'update' method updates the resource with the given id.*
>
>	*(this function is optional - raises by default* Exception(404, Not Found) )

    * arguments
<ul>
<li>  *self - self explanatory*</li>
<li>  *resource_id - the resources id - the resource to update with the concerning id*</li>
<li>  *data*</li>
</ul>
    * returns Object
<ul>
<li>  *serializable object - if given - the just updated entity*</li>
<li>  *None* return 'Internal Server Error', 500</li>
</ul>
    * raises Exception
<ul>
<li>  *exception.message - if given - defines the message of the http response*</li>
<li>  *exception.code - if given - defines the response code of the http response*</li>
</ul>

  * #### def delete(self, resource_id):
>	*The 'delete' method access the resource with the specified id.*
>
>	*(this function is optional - raises by default* Exception(404, Not Found) )

    * arguments
<ul>
<li>  *self - the object itself - self explanatory*</li>
<li>  *resource_id - the resources id - the resource to delete with the concerning id*</li>
</ul>
    * returns Boolean
<ul>
<li>  *True - if given - means the deletion of the concerning resource succeeded*</li>
<li>  *False - if given - means the deletion of the concerning resource failed*</li>
<li>  *None - means the deletion of the concerning resource failed*</li>
</ul>
    * raises Exception
<ul>
<li>  *exception.message - if given - defines the message of the http response*</li>
<li>  *exception.code - if given - defines the response code of the http response*</li>
</ul>


  * #### def health_check(self):
>	*Through the 'health_check' method you can perform some dependency checks*
>	*which should not fail to serve the provisioning*
>
>	*(this function is optional - returns by default* True )

    * arguments
<ul>
<li> *self - the object itself - self explanatory*</li>
</ul>
    * returns Boolean
<ul>
<li>  *True - if given - means the health_check succeeded and the server is reachable*</li>
<li>  *False - if given - means the health_check failed and the server is not reachable*</li>
<li>  *None - means the health_check failed and the server is not reachable*</li>
</ul>
    * raises Exception
<ul>
<li> *If an execption raises the server will be* HTTP 503 SERVICE UNAVAILABLE</li>
</ul>
