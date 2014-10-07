from setuptools import setup

setup(
    name='provisional',
    version='0.3',
    description='Flask skeleton app for add-on provisioning API',
    url='http://github.com/cloudControl/provisional-python',
    author='cloudControl Team',
    author_email='info@cloudcontrol.de',
    license='Apache 2.0',
    install_requires=[
        'flask>=0.7',
        'flask-sslify>=0.1.4'
    ],
    py_modules=['provisional'],
)
