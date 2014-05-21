'''
Created on Jan 17, 2014

@author: sean
'''
from flask import request
from flask import render_template
from flask import current_app
from os.path import basename, join, isfile, split, getmtime, dirname
from IPython.nbconvert.exporters import HTMLExporter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import mimetypes
import os


def raw_renderer(full_path):
    g = open(full_path)
    res = current_app.response_class(g, direct_passthrough=True)
    mimetype, _ = mimetypes.guess_type(full_path)

    if mimetype is None:
        mimetype = 'application/octet-stream'

    res.headers['Content-Type'] = mimetype
    return res


def nb_renderer(full_path):
    directory, base = split(full_path)
    cache_file = join(directory, '.%s.html' % base)
    if not current_app.config.get('DEBUG'):
        try:
            if isfile(cache_file) and getmtime(full_path) < getmtime(cache_file):
                current_app.logger.debug('Using Cache File %s' % cache_file)
                return raw_renderer(cache_file)
        except:
            current_app.logger.warn('There was an error reading from the cache file %s' % cache_file)

    ex = HTMLExporter(extra_loaders=[current_app.jinja_env.loader],
                      template_file='wakari_notebook.html')

    ex.environment.globals.update(current_app.jinja_env.globals)
    current_app.update_template_context(ex.environment.globals)
    ex.environment.globals.update(dirname=dirname(request.view_args['path']))

    output, _ = ex.from_filename(full_path)


    try:
        with open(cache_file, 'w') as fd:
            current_app.logger.debug('Writing Cache File %s' % cache_file)
            fd.write(output.encode(errors='replace'))
    except (OSError, IOError):
        current_app.logger.warn('There was an error writing to the cache file %s' % cache_file)
        try:
            if isfile(cache_file): os.unlink(cache_file)
        except OSError:
            current_app.logger.warn('There was an error removing the cache file %s' % cache_file)
            pass

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
