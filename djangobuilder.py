#   @name                 djangobuilder.py
#   @desc                 Builds custom Django project according to
#                         arguments passed through command line
#   @reqs                 python, virtualenv, virtualenvwrapper, git
#   @version              v0.2
#
#   @original_authors     Steve Phillips <steve@builtbyptm.com>
#                         AJ v Bahnken <aj@builtbyptm.com>
#   @personal_fork        Kevin Xu <kevin@imkevinxu.com>
#   @copyright            Apache License, Version 2.0



#
#   Python imports
#

import os
import random
import re
import shutil
import string
import sys

from subprocess import Popen, call, STDOUT, PIPE



#
#   Check for initial conditions
#

try:
    import argparse
except ImportError:
    print "argparse not installed. Please install with\n"
    print "    sudo pip install argparse\n"
    print "then re-run this script."
    sys.exit(1)

# If user is in a virtualenv, tell them to get out first
if hasattr(sys, 'real_prefix'):
    print "You're already in a virtualenv. Type\n"
    print "    deactivate\n"
    print "to leave, then run this script again."
    sys.exit(1)



#
#   General Functions
#

def sh(cmd):
    return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0]

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath and is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None



#
#   Functions related to project setup
#

def check_projectname():
    if not re.search(r'^[_a-zA-Z]\w*$', PROJECT_NAME):
        message = 'Error: \'%s\' is not a valid project name. Please ' % PROJECT_NAME
        if not re.search(r'^[_a-zA-Z]', PROJECT_NAME):
            message += ('make sure the name begins '
                        'with a letter or underscore.')
        else:
            message += 'use only numbers, letters and underscores.'

        sys.exit(message)

def find_virtualenvwrapper():
    path = which('virtualenvwrapper.sh')
    if path is None:
        path = '/usr/local/bin/virtualenvwrapper.sh'

    if not os.path.isfile(path):
        cmd = 'echo $VIRTUALENV_WRAPPER_PATH'
        output = call(cmd, shell=True)
        if output:
            path = output
        else:
            print "We can not seem to find virtualenvwrapper.sh\n"
            print "Either install it through pip\n"
            print "     sudo pip install virtualenvwrapper\n"
            print "or set $VIRTUALENV_WRAPPER_PATH to the location of\n"
            print "virtualenvwrapper.sh on your machine."
            sys.exit(1)
    return path



#
#   Functions related to copying and string interpolating
#   django and template files
#

# Imports extra settings related to extra packages
from extra_settings import *

# Copies the contents of django_files and server_scripts, and
# performs string interpolations (e.g., %(PROJECT_NAME)s => 'myapp')
def prepare_django_files(files):
    for filename in files:
        f_read = open(DJANGO_FILES_PATH + filename, 'r')
        contents = f_read.read()
        f_read.close()

        new_filename = filename.replace('-needed', '')
        for dir in django_pathify[new_filename]:

            # Appends certain attributes and settings to some django files for
            # various extra packages according to the arguments
            if ARGUMENTS.bcrypt and new_filename in bcryptify_files:
                contents = bcryptify(contents, new_filename)
            if ARGUMENTS.debug and new_filename in debugify_files:
                contents = debugify(contents, new_filename)
            if ARGUMENTS.jinja2 and new_filename in jinjaify_files:
                contents = jinjaify(contents, new_filename)

            # Justifies the spacing for comments in code in README.md
            if new_filename == "README.md":
                contents = justify(contents)

            new_contents = contents if "%s" in contents else contents % replacement_values

            file_path = dir % replacement_values
            f_write = open(PROJECT_PATH + file_path + new_filename, 'a')
            f_write.write(new_contents)
            f_write.close()

# Replace variables within the templates by performing custom
# string interpolations (e.g., %(PROJECT_NAME)s => 'myapp')
# because of existing % signs inside templating language
def prepare_template_files():
    templates_dir = PROJECT_PATH + 'templates/'
    template_files = [x for x in os.listdir(templates_dir)]
    for template in template_files:
        f_read = open(templates_dir + template, 'r')
        contents = f_read.read()
        f_read.close()

        f_write = open(templates_dir + template, 'w')
        for key, value in replacement_values.items():
            contents = contents.replace('%(' + key + ')s', value)

        if ARGUMENTS.theme == 'foundation':
            if ARGUMENTS.bcrypt and template in bcryptify_files:
                contents = bcryptify(contents, template)
            if ARGUMENTS.debug and template in debugify_files:
                contents = debugify(contents, template)
            if ARGUMENTS.jinja2 and template in jinjaify_template_files:
                contents = jinjaify_templates(contents, template)

        f_write.write(contents)
        f_write.close()



#
#   Parses command line for arguments
#

def parse_arguments():
    parser = argparse.ArgumentParser(description='''Django Project Builder is the
                        fastest, easiest way to build a new Django project''')

    # Simple arguments
    parser.add_argument('--version', '-v', action='version',
                        version='Django Project Builder v0.2')
    parser.add_argument('--path', action='store', dest='path',
                        help='''Specifies where the new Django project
                        should be made, including the project name at the
                        end (e.g. /home/username/code/project_name)''',
                        required=True)
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='''Quiets all output except the finish message.''',
                        dest='quiet')

    # Theme choice argument
    parser.add_argument('--theme', action='store', default=False,
                        choices=['bootstrap', 'foundation'],
                        help='''This will include an frontend theme for CSS/JS
                        like Bootstrap, Foundation, or Generic.''', dest='theme')

    # Extra Packages
    parser.add_argument('--bcrypt', action='store_true', default=False,
                        help='''This will install py-bcrypt and use bcrypt
                        as the main password hashing for the project.''', dest='bcrypt')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='''This will install the Django Debug Toolbar
                        package for the project.''', dest='debug')
    parser.add_argument('--jinja2', action='store_true', default=False,
                        help='''This will install Jinja2 and Coffin as the default
                        templating engine of the project.''', dest='jinja2')

    # SUPER Argument for imkevinxu
    parser.add_argument('--imkevinxu', action='store_true', default=False,
                        help='''Super argument with default packages for imkevinxu
                        using his favorite best practices''',
                        dest='imkevinxu')

    arguments = parser.parse_args()

    # All arguments that --imkevinxu enables
    if arguments.imkevinxu:
        arguments.theme = 'foundation'
        arguments.jinja2 = True
        arguments.bcrypt = True
        arguments.debug = True

    return arguments



#
#   Global Variables
#

# Arguments passed from command line
ARGUMENTS = parse_arguments()

# Django paths
DPB_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
DJANGO_FILES_PATH = DPB_PATH + 'django-files/'
VIRTUALENV_WRAPPER_PATH = find_virtualenvwrapper()

# Trailing / may be included or excluded up to this point
PROJECT_PATH = ARGUMENTS.path.rstrip('/') + '/'
PROJECT_NAME = PROJECT_PATH.split('/')[-2].split('_')[0]  # Before the '/'
BASE_PATH    = '/'.join(PROJECT_PATH.split('/')[:-2]) + '/'

# Admin Information
ADMIN_NAME  = os.environ.get("ADMIN_NAME") if os.environ.get("ADMIN_NAME") else 'Agent Smith'
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") if os.environ.get("ADMIN_EMAIL") else 'admin@example.com'
SECRET_KEY  = ''.join([random.choice(string.printable[:94].replace("'", ""))
                      for _ in range(50)])
PROJECT_PASSWORD = ''.join([random.choice(string.printable[:62])
                            for _ in range(30)])

# Maps cleaned filenames to where each file should be copied relative to PROJECT_PATH
django_pathify = {
    '.env':                         [''],
    '.env.dev':                     [''],
    '.foreman':                     [''],
    '.gitignore':                   [''],
    '__init__.py':                  ['%(PROJECT_NAME)s/', '%(CONFIG_NAME)s/'],
    'admin.py':                     ['%(PROJECT_NAME)s/'],
    'appurls.py':                   ['%(PROJECT_NAME)s/'],
    'django.wsgi':                  ['apache/'],
    'forms.py':                     ['%(PROJECT_NAME)s/'],
    'jinja2.py':                    ['%(CONFIG_NAME)s/'],
    'manage.py':                    [''],
    'model_forms.py':               ['%(PROJECT_NAME)s/'],
    'models.py':                    ['%(PROJECT_NAME)s/'],
    'notes.txt':                    [''],
    'Procfile':                     [''],
    'Procfile.dev':                 [''],
    'README.md':                    [''],
    'requirements.txt':             [''],
    'settings.py':                  ['%(CONFIG_NAME)s/'],
    'settings_local.py':            ['%(CONFIG_NAME)s/'],
    'tests.py':                     ['%(PROJECT_NAME)s/'],
    'urls.py':                      ['%(CONFIG_NAME)s/'],
    'views.py':                     ['%(PROJECT_NAME)s/'],
    'wsgi.py':                      ['%(CONFIG_NAME)s/'],
}

# Defines key: value pairs so that
#   '%(PROJECT_NAME)s' % replacement_values
# evaluates to the value of the `PROJECT_NAME` variable, such as
#   'my_project_name'
replacement_values = {
    'PROJECT_NAME':     PROJECT_NAME,
    'PROJECT_NAME_CAP': PROJECT_NAME.capitalize(),
    'PROJECT_PASSWORD': PROJECT_PASSWORD,
    'BASE_PATH':        BASE_PATH,
    'SECRET_KEY':       SECRET_KEY,
    'PROJECT_PATH':     PROJECT_PATH,
    'ADMIN_NAME':       ADMIN_NAME,
    'ADMIN_EMAIL':      ADMIN_EMAIL,
    'CONFIG_NAME':      'config',
}



#
#   Builds Django Project
#

def build():

    #
    #   Make sure PROJECT_NAME follows Django's restrictions
    #

    check_projectname()

    #
    #   Creates project folder and initializes git repo
    #

    if not ARGUMENTS.quiet:
        print "\nCreating %s..." % PROJECT_NAME

    # Use 'git init' to create the PROJECT_PATH directory and turn it into a git repo
    cmd = 'bash -c "git init %s"' % PROJECT_PATH
    output = sh(cmd)



    #
    #   Creates django directories and performs
    #   string interpoliation on all django files
    #

    if not ARGUMENTS.quiet:
        print "Creating django files..."

    # Django-related folders inside project
    project_dirs = ['static', 'apache', '%(CONFIG_NAME)s', '%(PROJECT_NAME)s']

    for dir_name in project_dirs:
        os.mkdir(PROJECT_PATH + dir_name % replacement_values)

    # Django-related files to be copied into new project
    django_files = [x for x in os.listdir(DJANGO_FILES_PATH) if x.endswith('-needed')]

    if not ARGUMENTS.jinja2:
        django_files.remove('jinja2.py-needed')

    prepare_django_files(django_files)



    #
    #   Creates static and template directories and performs
    #   string interpolation on all template files
    #

    if not ARGUMENTS.quiet:
        print "Creating static and template files..."

    # Static and template directory names here
    generic_dirs = ['static', 'templates']
    generic_dirs = [DPB_PATH + d for d in generic_dirs]

    # Recursively copies static and template files into respective folders
    for dirname in generic_dirs:
        new_dir = PROJECT_PATH + dirname.split('/')[-1]
        if not ARGUMENTS.theme:
            shutil.copytree(dirname + '-generic', new_dir)
        else:
            shutil.copytree(dirname + '-' + ARGUMENTS.theme, new_dir)

    prepare_template_files()



    #
    #   Creates the project's virtual environment
    #

    if not ARGUMENTS.quiet:
        print "Creating virtualenv..."

    cmd  = 'bash -c "source %s &&' % VIRTUALENV_WRAPPER_PATH
    cmd += ' mkvirtualenv %s"' % PROJECT_NAME

    output = sh(cmd)

    if not ARGUMENTS.quiet:
        print '\n', output



    #
    #   Installs python packages from requirements.txt inside the project's
    #   virtualenv and collects static assets
    #

    if not ARGUMENTS.quiet:
        print "Running 'pip install -r requirements.txt'. This could take a while...",
        print "(don't press control-c!)"

    cmd  = 'bash -c "source %s && workon' % VIRTUALENV_WRAPPER_PATH
    cmd += ' %(PROJECT_NAME)s && cd %(PROJECT_PATH)s &&' % replacement_values
    cmd += ' pip install -r requirements.txt && pip freeze > requirements.txt'
    cmd += ' && python manage.py collectstatic --noinput"'

    output = sh(cmd)

    if not ARGUMENTS.quiet:
        print '\n', output



    #
    #   First commit
    #

    if not ARGUMENTS.quiet:
        print "Creating git repo..."

    cmd  = 'bash -c "cd %s &&' % PROJECT_PATH
    cmd += ' git add . && git commit -m \'first commit\'"'
    output = sh(cmd)

    if not ARGUMENTS.quiet:
        print '\n', output



    #
    #   Complete!
    #

    print "Complete! Now run\n"
    print "    cd %(PROJECT_PATH)s && workon %(PROJECT_NAME)s &&" % replacement_values,
    print "python manage.py syncdb\n\nGet to work!"



#
#   Command Line Interface
#

if __name__ == '__main__':
    build()