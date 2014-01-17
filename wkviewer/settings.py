import os as _os

APP_CDN = None
CDN = 'https://wakari-static.s3.amazonaws.com/latest'
WOC = 'http://localhost:5000'
URL_PREFIX = ''
PROJECT_DIR = _os.path.abspath(_os.getcwd())



def config_files(filename=None):
    import sys
    from os.path import isfile, join

    dirs = ['/etc/wakari', join(sys.prefix, 'etc/wakari'), '.']
    filenames = ['config.json', 'viewer-config.json']
    
    for CONFIG_DIR in dirs:
        for CONFIG_NAME in filenames: 
            CONFIG_PLACE = join(CONFIG_DIR, CONFIG_NAME)
            if isfile(CONFIG_PLACE):
                yield CONFIG_PLACE
                
    if filename is not None:
        yield filename

def update(filename=None, **kwargs):
    import json
    for CONFIG_PLACE in config_files(filename):
        filename = CONFIG_PLACE
        print 'Loading config from %s' % (filename,)

        with open(filename) as fp:
            data = json.load(fp)

        globals().update(kwargs)
        globals().update(data)
