'''
Created on Jan 13, 2014

@author: sean
'''
from wkviewer import settings as app_settings
from flask import Flask, url_for
from argparse import ArgumentParser
import os
from flask import render_template

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
    return render_template('404.html')

def make_app(project_dir, url_prefix):
    app_args = {}
    
    
    if app_settings.APP_CDN is None:
        app_args['static_folder'] = project_dir
        app_args['static_url_path'] = url_prefix

    app = Flask(__name__, template_folder='templates', **app_args)
    app.config.from_object(app_settings)

    app.url_map.strict_slashes = False
    app.config.update(HOME_DIR=project_dir)
    
    app.context_processor(context_processor)

    print "app.errorhandler"
    app.errorhandler(404)(handle404)

    return app


def main():
    parser = ArgumentParser(description='Wakari Workbench')
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--url-prefix', default='')
    parser.add_argument('--project-dir', default=os.getcwd())
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    
    app_settings.update(DEBUG=args.debug)
    
    app = make_app(args.project_dir, args.url_prefix)

    app.run(host='localhost', port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
