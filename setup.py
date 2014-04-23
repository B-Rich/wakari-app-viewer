from setuptools import setup

try:
    from wkviewer import __version__ as version
except ImportError:
    version = '???'

setup(
    name='wakari-app-viewer',
    version=version,
    author='Continuum Analytics',
    author_email='wakari-dev@continuum.io',
    description='Wakari Read-only File viewer application',
    packages=['wkviewer'],
    install_requires=['Flask', 'werkzeug', 'ipython', 'pygments'],
    include_package_data=True,
    package_data={'wkviewer': ['templates/*']},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'wk-app-viewer = wkviewer.server:main'
            ]
    }
)
