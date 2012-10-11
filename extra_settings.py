#!/usr/bin/env python

# Function that justifies the comments to start at 70 characters
# no matter how long the piece of code is in the README.md
def justify(contents):
    buf = contents.split('\n')
    for i, b in enumerate(buf):
        if b[0:4] == '    ' and b[4] != '#' and b.find('#') > 0:
            end = b.find('#')
            justify = b[:end].ljust(70)
            buf[i] = justify + b[end:]
    return '\n'.join(buf)

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]

# Files and function to add the right settings to enable bcrypt password hashing
bcryptify_files = ['requirements.txt', 'settings.py', 'index.html', 'README.md']
def bcryptify(contents, filename):
    if filename == 'requirements.txt':
        contents += '\npy-bcrypt==0.2'
    elif filename == 'settings.py':
        new  = "PASSWORD_HASHERS = (\n"
        new += "    'django.contrib.auth.hashers.BCryptPasswordHasher',\n"
        new += "    'django.contrib.auth.hashers.PBKDF2PasswordHasher',\n"
        new += "    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',\n"
        new += "    'django.contrib.auth.hashers.SHA1PasswordHasher',\n"
        new += "    'django.contrib.auth.hashers.MD5PasswordHasher',\n"
        new += "    'django.contrib.auth.hashers.CryptPasswordHasher',\n"
        new += ")\n\n"
        keyword = 'MIDDLEWARE_CLASSES'
        pos = contents.find(keyword)
        contents = insert(contents, new, pos)

    elif filename == 'index.html':
        keyword = '</h5>'
        pos = contents.find(keyword)+len(keyword)+2
        new = '            <li style="margin-left:35px"><h5>'
        new += '<a href="https://docs.djangoproject.com/en/dev/topics/auth/#using-bcrypt-with-django" '
        new += 'target="_blank">bcrypt</a> password hashing enabled</h5></li>\n\n'
        contents = insert(contents, new, pos)
    elif filename == 'README.md':
        keyword = 'Customizations'
        pos = contents.find(keyword)+len(keyword)+2
        new = '* [bcrypt](https://docs.djangoproject.com/en/dev/topics/auth/#using-bcrypt-with-django) password hashing\n'
        contents = insert(contents, new, pos)

    return contents

# Files and function to add the right settings to enable Django Debug Toolbar
debugify_files = ['requirements.txt', 'settings.py', 'index.html', 'README.md']
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

    elif filename == 'index.html':
        keyword = '</h5>'
        pos = contents.find(keyword)+len(keyword)+2
        new = '            <li style="margin-left:35px"><h5>'
        new += '<a href="https://github.com/django-debug-toolbar/django-debug-toolbar" '
        new += 'target="_blank">Django Debug Toolbar</a> enabled</h5></li>\n\n'
        contents = insert(contents, new, pos)
    elif filename == 'README.md':
        keyword = 'Customizations'
        pos = contents.find(keyword)+len(keyword)+2
        new = '* [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)\n'
        contents = insert(contents, new, pos)

    return contents

# Files and function to add the right settings to enable Jinja2 as the default
# templating engine using Coffin as an adapter
jinjaify_files = ['requirements.txt', 'settings.py', 'views.py', 'urls.py', 'appurls.py', 'README.md']
def jinjaify(contents, filename):
    if filename == 'requirements.txt':
        contents += '\nJinja2==2.6'
        contents += '\nCoffin==0.3.7'
    elif filename == 'settings.py':
        new = "    'coffin',\n"
        keyword = 'south'
        pos = contents.find(keyword)+len(keyword)+3
        contents = insert(contents, new, pos)
    elif filename == 'views.py':
        contents = contents.replace('django.shortcuts', 'coffin.shortcuts')
    elif filename == 'urls.py':
        contents = contents.replace('django.conf.urls.defaults', 'coffin.conf.urls.defaults')
    elif filename == 'appurls.py':
        contents = contents.replace('django.conf.urls.defaults', 'coffin.conf.urls.defaults')
        contents = contents.replace('django.shortcuts', 'coffin.shortcuts')
        contents = contents.replace('login, logout', 'logout')
        keyword = 'logout'
        pos = contents.find(keyword)+len(keyword)+2
        new = 'from %(PROJECT_NAME)s.jinja2 import login\n\n'
        contents = insert(contents, new, pos)

    elif filename == 'README.md':
        keyword = 'Customizations'
        pos = contents.find(keyword)+len(keyword)+2
        new = '* [Jinja2](http://jinja.pocoo.org/docs/) templating with [Coffin](https://github.com/coffin/coffin)\n'
        contents = insert(contents, new, pos)

    return contents

# Files and function to edit certain template tags in the templates to work with Jinja2
jinjaify_template_files = ['base.html', 'index.html', 'template.html', 'login.html']
def jinjaify_templates(contents, filename):
    contents = contents.replace('block.super', 'super()')
    if filename == 'index.html':
        keyword = '</h5>'
        pos = contents.find(keyword)+len(keyword)+2
        new = '            {% set template = "<a href=\\"http://jinja.pocoo.org/docs/\\" target=\\"_blank\\">Jinja2</a>" %}\n'
        new += '            <li style="margin-left:35px"><h5>{{ template|safe }} templating engine enabled with '
        new += '<a href="https://github.com/coffin/coffin" target="_blank">Coffin</a></h5></li>\n\n'
        contents = insert(contents, new, pos)
    elif filename == 'base.html':
        contents = contents.replace('user.is_authenticated', 'user.is_authenticated()')
    elif filename == 'login.html':
        contents = contents.replace('form.as_ul', 'form.as_ul()|safe')

    return contents
