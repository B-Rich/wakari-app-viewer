import sys

if 'develop' in sys.argv:
    # Don't import setuptools unless the user is actively trying to do
    # something that requires it.
    from setuptools import setup

else:
    from distutils.core import setup

try:
    from wkviewer import __version__ as version
except ImportError:
    version = '???'
    
setup(
    name='wk-viewer',
    version=version,
    author='Continuum Analytics',
    author_email='wakari-dev@continuum.io',
    description='Wakari Read-only File viewer application',
    packages=['wkviewer'],
    install_requires=['Flask', 'werkzeug'],
    include_package_data=True,
    package_data = {'wkviewer':['templates/*']},
    zip_safe=False,
    entry_points = {
        'console_scripts' : [
            'wk-viewer = wkviewer.server:main'
            ]
    }
)
