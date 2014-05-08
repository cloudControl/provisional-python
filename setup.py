from setuptools import setup

setup(
    name='provisional',
    version='0.2',
    description='Flask skeleton app for add-on provisioning API',
    url='http://github.com/cloudControl/provisional-python',
    author='cloudControl Team',
    author_email='info@cloudcontrol.de',
    license='Apache 2.0',
    install_requires=['flask'],
    py_modules=['provisional'],
)
