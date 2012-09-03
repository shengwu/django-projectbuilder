#!/usr/bin/env python

def insert(original, new, pos):
  '''Inserts new inside original at pos.'''
  return original[:pos] + new + original[pos:]

def justify(contents):
    buf = contents.split('\n')
    for i, b in enumerate(buf):
        if b[0:4] == '    ' and b[4] != '#' and b.find('#') > 0:
            end = b.find('#')
            justify = b[:end].ljust(70)
            buf[i] = justify + b[end:]
    return '\n'.join(buf)

debugify_files = ['requirements.txt', 'settings.py']

def debugify(contents, filename):
    if filename == 'requirements.txt':
        contents += '\ndjango-debug-toolbar==0.9.4'
    elif filename == 'settings.py':
        new = "    'debug_toolbar',\n"
        keyword = 'south'
        pos = contents.find(keyword)+len(keyword)+3
        contents = insert(contents, new, pos)

        new  = "    # Comment the next line to disable the Django Debug Toolbar\n"
        new += "    'debug_toolbar.middleware.DebugToolbarMiddleware',\n"
        keyword = 'XFrameOptionsMiddleware'
        pos = contents.find(keyword)+len(keyword)+3
        contents = insert(contents, new, pos)

        pos += len(new)+3
        new  = "DEBUG_TOOLBAR_CONFIG = {\n"
        new += "    'INTERCEPT_REDIRECTS' : False,\n"
        new += "}\n\n"
        contents = insert(contents, new, pos)
    return contents

jinjaify_files = ['requirements.txt', 'settings.py', 'urls.py', 'appurls.py', 'views.py', 'README.md']

def jinjaify(contents, filename, replacement_values=None):
    if filename == 'requirements.txt':
        contents += '\nJinja2==2.6'
        contents += '\nhttps://github.com/coffin/coffin/zipball/master'
    elif filename == 'settings.py':
        new = "    'coffin',\n"
        keyword = 'south'
        pos = contents.find(keyword)+len(keyword)+3
        contents = insert(contents, new, pos)
    elif filename == 'urls.py' or filename == 'appurls.py':
        contents = contents.replace('django.conf.urls.defaults', 'coffin.conf.urls.defaults')
    elif filename == 'views.py':
        contents = contents.replace('django.shortcuts', 'coffin.shortcuts')
    elif filename == 'README.md':
        new = "    pip install https://github.com/coffin/coffin/zipball/master #Coffin v0.3.7-dev must be manually installed\n"
        keyword = 'virtual environment'
        pos = contents.find(keyword)+len(keyword)+2
        contents = insert(contents, new, pos)

        new  = "\n\n### Coffin/Jinja2 Module Errors\n\n"
        new += "Either you're missing [Coffin](https://github.com/coffin/coffin) or \
have an outdated version from [PyPI](http://pypi.python.org/pypi/Coffin). \
PyPI currently hosts v0.3.6 but this Django project needs v0.3.7-dev from \
the Github repo.\n\n"
        new += "Please run this code while working in the `%(PROJECT_NAME)s` virtual environment:\n\n" % replacement_values
        new += "    pip install https://github.com/coffin/coffin/zipball/master"
        contents += new

    return contents