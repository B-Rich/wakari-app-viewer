'''
Created on Jan 17, 2014

@author: sean
'''

from wkviewer import settings as app_settings
from flask import Blueprint, request
import os
from flask import render_template
from flask import abort
from os.path import basename, join, isdir, isfile, dirname
from urllib import quote
import re
from wkviewer.renderer import get_renderer, raw_renderer


blueprint = Blueprint('viewer', __name__)

def filter_files(top, pat, files):
    pat = re.escape(pat).replace('\*', '.*')
    cpat = re.compile(pat)
    i = 0; j = 0;  # Limit the number of files searched so the request does not hang
    
    baselen = len(top)
    if not top.endswith('/'):
        baselen += 1
         
    for dirpath, dirnames, filenames in files:
        if '/.' in dirpath: continue
        for dirname in dirnames:
            j += 1
            if dirname.startswith('.'): continue
            if cpat.match(dirname):
                yield True, join(dirpath, dirname)[baselen:]
                i += 1; 
                if i > 100: return
        
        for filename in filenames:
            j += 1
            if filename.startswith('.'): continue
            
            if cpat.match(filename):
                yield False, join(dirpath, filename)[baselen:]
                i += 1; 
                if i > 100: return
                
        if j > 50000: return  # 50000 files is enough
        
        
@blueprint.route('/search')
def search(path=''):
    pat = request.args.get('glob')
    print 'app_settings.PROJECT_DIR', app_settings.PROJECT_DIR
    top = app_settings.PROJECT_DIR
    if pat:
        files = os.walk(top)
        listing = filter_files(top, pat, files)
    else:
        listing = None
        
    return render_template('search.html', listing=listing,
                           pat=pat)

@blueprint.route('/')
@blueprint.route('/<path:path>')
def content(path=''):
    full_path = os.path.join(app_settings.PROJECT_DIR, path)

    if isdir(full_path):
        project_dirbase = basename(app_settings.URL_PREFIX)
        dirpath = join(project_dirbase, path)
        dirs = [(app_settings.URL_PREFIX or '', project_dirbase)]
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
