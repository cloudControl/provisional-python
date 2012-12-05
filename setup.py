from setuptools import setup

setup(name='provisional',
      version='0.1',
      description=open('README.md').read(),
      url='http://github.com/cloudControl/provisional-python',
      author='cloudControl Team',
      author_email='info@cloudcontrol.de',
      license='Apache 2.0',
      install_requires=[pkg for pkg in open('requirements.txt')],
      packages=['provisional'],
      )
