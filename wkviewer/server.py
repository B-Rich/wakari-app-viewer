'''
Created on Jan 13, 2014

@author: sean
'''
from wkviewer import settings as app_settings
from flask import Flask, url_for, request
from argparse import ArgumentParser
import os
from flask import render_template
from flask import current_app
from os.path import dirname
import getpass
import views

def static(filename):
    if app_settings.APP_CDN:
        return '%s/%s' % (app_settings.APP_CDN, filename)
    else:
        return url_for('static', filename=filename)

def context_processor():
    d = {}
    d['static'] = static
    d['CDN'] = app_settings.CDN
    d['WOC'] = app_settings.WOC
    return d

def handle404(err):
    path = request.path[len(app_settings.URL_PREFIX) + 1:]
    return render_template('404.html',
                           path=path,
                           up=dirname(path),
                           user=getpass.getuser(),
                           )


def handle500(err):
    path = request.path[len(app_settings.URL_PREFIX) + 1:]
    return render_template('500.html',
                           path=path,
                           up=dirname(path),
                           user=getpass.getuser(),
                           )


def make_app(project_dir, url_prefix):
    app_args = {}
    
    app = Flask(__name__, template_folder='templates', **app_args)
    app.config.from_object(app_settings)

    app.url_map.strict_slashes = False
    app.config.update(HOME_DIR=project_dir)
    
    views.blueprint.register(app, {'url_prefix': url_prefix})
    app.context_processor(context_processor)

    app.errorhandler(404)(handle404)
    app.errorhandler(500)(handle500)

    return app


def main():
    parser = ArgumentParser(description='Wakari Workbench')
    parser.add_argument('-p', '--port', default=5000, type=int)
    parser.add_argument('--url-prefix', default=app_settings.URL_PREFIX)
    parser.add_argument('--project-dir', default=app_settings.PROJECT_DIR)
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    
    app_settings.update(DEBUG=args.debug,
                        URL_PREFIX=args.url_prefix,
                        PROJECT_DIR=args.project_dir,
                        )
    
    app = make_app(args.project_dir, args.url_prefix)

    app.run(host='localhost', port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
