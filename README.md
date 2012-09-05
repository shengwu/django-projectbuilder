[Django Project Builder](http://builtbyptm.com/blog/announcing-django-project-builder-v01/ "Announcing Django Project Builder v0.1")
======================

## Introduction

Django Project Builder is the fastest, easiest way to, well... build a
new Django project!

### Features and Benefits

* Create a new Django project, git repo, virtualenv, and Django app
  with sane defaults and best practices _all_ with a single command

* Prepare your server for deployment with a couple more commands

* Auto-deploy your shiny new Django app to your server with a simple
  `git push`!  (Uses git hooks behind the scenes... but you don't need
  to worry about that, do you?)

* Three Front-end options, both with CSS Stylesheets and HTML Templates with a lot of swag.

* A bunch of extra packages and apps to go with your Django project

### Who is DPB for?

Django programmers using a Unix-based OS looking to do more coding and less config.

For those looking to enjoy convenient server deployments, note that
the __server scripts__ currently assume you're using Bash + virtualenv +
virtualenvwrapper + Ubuntu + Apache.  We're working on reducing the
number of dependencies.

[See our TODO](https://github.com/prototypemagic/django-projectbuilder/blob/master/TODO.md)
for what's on the horizon, and for what you may want to help out with.


## Local Development Instructions

### Installing Dependencies

If you're on a Mac (only been tested with OSX 10.7 Lion so far) and are missing
some dependencies like `pip`, `django`, `virtualenv`, or `virtualenvwrapper`
then `cd` into the django-projectbuilder repo and run

    source install_dependencies.sh

### Local Development Usage

After cloning this repo to your local machine, `cd` into it and run
something like

    python djangobuilder.py --path ~/new_project

to create the `~/new_project_site` directory, which contains _tons_ of
Django boilerplate -- common imports, virtualenv creation, a new git
repo, and more! `virtualenv` and `virtualenvwrapper` are required. `git` is
recommended. Django is awesome.

### Themes

If you add the optional `--bootstrap` argument, your project will be created
using all Bootstrap defaults for the front-end.

    python djangobuilder.py --path ~/new_project --bootstrap

If you add the optional `--foundation` argument, your project will be created
using all Foundation 3 defaults for the front-end including [Responsive Tables](http://www.zurb.com/playground/responsive-tables)
and the [Foundation Icons](http://www.zurb.com/playground/foundation-icons)

    python djangobuilder.py --path ~/new_project --foundation

### Extra packages

If you add the optional `--bcrypt` argument, your project will be created
using bcrypt as the default password hashing

    python djangobuilder.py --path ~/new_project --bcrypt

If you add the optional `--debug` argument, your project will be created
with the super handy Django Debug Toolbar

    python djangobuilder.py --path ~/new_project --debug

If you add the optional `--jinja2` argument, your project will be created
using Jinja2 as the default Templating engine with Coffin as the adapter

    python djangobuilder.py --path ~/new_project --jinja2


## Production Instructions

### Server Usage

After cloning this repo to one of your many servers, `cd` into it and
run

    bash gitbuilder.sh ~/new_project

to create the top-level project directory, bare git repo, and empty
${PROJECT_NAME}_site directory for the soon-to-exist Django project.
Follow the instructions echoed to the screen, which include using
`apachebuilder.sh` to generate your project's Apache config.

### Heroku Usage

Heroku requires that you use Postgres as your database.  To install
Postgres, run

    pip install psycopg2 dj-database-url

then add psycopg2, dj-database-url and every other Python module in your virtualenv to requirements.txt with

    pip freeze > requirements.txt

You also need to add the following to your `settings.py` for Heroku to use the right database
when you're in production. It's suggested to append this with an `else:` at the bottom of
`settings.py` so it is only run on the production server rather than locally

    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

Now add and commit your changes to the git repo

    git add * && git commit -m "Initial Heroku Deploy preparation complete!"

Create your new Heroku server with

    heroku create

In order for the app to know Heroku is a production server, this line of code
will add a heroku config variable for `PRODUCTION` so settings configure accordingly
with os.environ.get()

    heroku config:add PRODUCTION=True

and adding this config variable will make it easier to turn `DEBUG` on without redeploying

    heroku config:add DEBUG=False

Take a deep breath. Deploy away!

    git push heroku master

Finally run this line of code to sync the Django models with the database schema

    heroku run python manage.py syncdb

Make sure you also:

* Add any API Secret Keys as heroku config variables
* Migrate any apps on the database
* Configure any custom domains

See
[Getting Started with Django on Heroku/Cedar](https://devcenter.heroku.com/articles/django)
for more on deploying to Heroku.

### Auto Initial Heroku Deploy

To automate the above steps for your initial Heroku deploy,
`cd` into django-projectbuilder repo and run

    source initial_heroku_deploy.sh


## Troubleshooting

### Postgres

On Ubuntu, install Postgres with

    sudo apt-get install postgresql-server-dev-all

To install `psycopg2`, Django's Postgres driver, run

    pip install psycopg2

If you get the following error when trying to install `psycopg2`

    ./psycopg/psycopg.h:30:20: fatal error: Python.h: No such file or directory
    compilation terminated.
    error: command 'gcc' failed with exit status 1

that means you haven't installed all the necessary header (*.h) files
to compile additional Python modules/Django apps.  On Ubuntu, run

    sudo apt-get install python-dev

to fix this issue, then again try running

    pip install psycopg2

from within your project's virtualenv to install `psycopg2`.

### Questions?

If you run into any other issues, please let us know!
