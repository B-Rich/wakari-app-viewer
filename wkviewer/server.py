'''
Created on Jan 13, 2014

@author: sean
'''
from wkviewer import settings as app_settings
from flask import Flask, url_for, Blueprint, request
from argparse import ArgumentParser
import os
from flask import render_template
from flask import current_app, abort
from os.path import basename, join, isdir, isfile, split, getmtime, dirname
from IPython.nbconvert.exporters import HTMLExporter
from urllib import quote
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import getpass
import re

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
    path = request.path[len(current_app.config['URL_PREFIX']) + 1:]
    return render_template('404.html',
                           path=path,
                           up=dirname(path),
                           user=getpass.getuser(),
                           )

blueprint = Blueprint('viewer', __name__)

def raw_renderer(full_path):
    g = open(full_path)
    res = current_app.response_class(g, direct_passthrough=True)
    res.headers['Content-Type'] = 'text/plain'
    return res


def nb_renderer(full_path):
    directory, base = split(full_path)
    cache_file = join(directory, '.%s.html' % base)
    if not current_app.config.get('DEBUG'):
        try:
            if isfile(cache_file) and getmtime(full_path) < getmtime(cache_file):
                current_app.logger.debug('Using Cache File')
                return raw_renderer(cache_file)
        except:
            current_app.logger.warn('There was an error reading from the cache file')
    
    ex = HTMLExporter(extra_loaders=[current_app.jinja_env.loader],
                      template_file='wakari_notebook.html')
    
    ex.environment.globals.update(current_app.jinja_env.globals)
    current_app.update_template_context(ex.environment.globals)
    ex.environment.globals.update(dirname=dirname(request.view_args['path']))
    
    output, _ = ex.from_filename(full_path)
    
    try:
        with open(cache_file, 'w') as fd:
            current_app.logger.debug('Writing Cache File')
            fd.write(output)
    except:
        current_app.logger.warn('There was an error writing to the cache file')
        
    return output
    
def pygments_renderer(full_path):
    lexer = get_lexer_for_filename(full_path)
    formatter = HtmlFormatter(linenos=True, 
                              anchorlinenos=True,
                              cssclass="source")
    with open(full_path) as fd:
        code = highlight(fd.read(), lexer, formatter)
        
    return render_template('code.html', code=code,
                           up=dirname(request.view_args['path']),
                           name=basename(full_path),
                           )

def get_renderer(full_path):
    if full_path.endswith('.ipynb'):
        return nb_renderer
    else:
        try:
            get_lexer_for_filename(full_path)
            return pygments_renderer 
        except ClassNotFound:
            return raw_renderer
        
    return raw_renderer


def filter_files(top, pat, files):
    print re.escape(pat)
    pat = re.escape(pat).replace('\*', '.*')
    print pat
    cpat = re.compile(pat)
    
    for dirpath, dirnames, filenames in files:
        if '/.' in dirpath: continue
        for dirname in dirnames:
            if dirname.startswith('.'): continue
            if cpat.match(dirname):
                yield True, join(dirpath, dirname)[len(top) + 1:]
        
        for filename in filenames:
            if filename.startswith('.'): continue
            
            print pat, filename
            if cpat.match(filename):
                yield False, join(dirpath, filename)[len(top) + 1:]
        
        
@blueprint.route('/search')
def search(path=''):
    pat = request.args.get('glob')
    top = current_app.config['PROJECT_DIR']
    files = os.walk(top)
    listing = filter_files(top, pat, files)
    return render_template('search.html', listing=listing,
                           pat=pat)

@blueprint.route('/')
@blueprint.route('/<path:path>')
def content(path=''):
    full_path = os.path.join(current_app.config['PROJECT_DIR'], path)

    if isdir(full_path):
        project_dirbase = basename(current_app.config['PROJECT_DIR'])
        dirpath = join(project_dirbase, path)
        dirs = [(current_app.config['URL_PREFIX'], project_dirbase)]
        for d in path.split(os.sep):
            if d:
                prev = join(dirs[-1][0], quote(d))
                dirs.append((prev, d))
                
        is_dir = lambda item: isdir(join(full_path, item))
        
        contents = [(is_dir(item), item) for item in sorted(os.listdir(full_path)) if not item.startswith('.')]
        
        return render_template('directory.html',
                               filename=basename(path),
                               dirpath=dirpath,
                               up=dirname(path),
                               name=dirpath,
                               dirs=dirs[::-1],
                               contents=contents)
    elif isfile(full_path):
        if request.args.get('raw'):
            renderer = raw_renderer
        else:
            renderer = get_renderer(full_path)
            
        return renderer(full_path)
    else:
        abort(404)

def make_app(project_dir, url_prefix):
    app_args = {}
    
    app = Flask(__name__, template_folder='templates', **app_args)
    app.config.from_object(app_settings)

    app.url_map.strict_slashes = False
    app.config.update(HOME_DIR=project_dir)
    
    blueprint.register(app, {'url_prefix': url_prefix})
    app.context_processor(context_processor)

    app.errorhandler(404)(handle404)

    return app


def main():
    parser = ArgumentParser(description='Wakari Workbench')
    parser.add_argument('-p', '--port', default=5000, type=int)
    parser.add_argument('--url-prefix', default='')
    parser.add_argument('--project-dir', default=os.getcwd())
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
