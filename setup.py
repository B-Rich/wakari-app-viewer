import sys

if 'develop' in sys.argv:
    # Don't import setuptools unless the user is actively trying to do
    # something that requires it.
    from setuptools import setup

else:
    from distutils.core import setup


setup(
    name='wk-viewer',
    version="1.0.0",
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
