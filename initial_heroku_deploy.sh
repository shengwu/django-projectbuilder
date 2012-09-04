#!/bin/sh
# Kevin Xu / imkevinxu
# 2012.08.28

# Script for initial push to Heroku

# Detects if the user has heroku installed and prompts them to install it if not
if [ -z `which heroku` ]; then
    
    echo "Detected heroku has not been installed"
    echo "INSTALL heroku here https://devcenter.heroku.com/articles/quickstart"

else

    # Proceed if user is working in a virtualenv
    if [ -d "$VIRTUAL_ENV" ]; then

         # Proceed if user is currently in the top level directory of the project
        if [ -s "manage.py" ]; then

            # Prompts user for a name of the heroku app
            echo "Starting Initial Heroku Deploy!"
            echo
            read -p "    # What will you name the new Heroku app? (leave blank for random name) "
            HEROKU_NAME=$REPLY

            echo
            echo "[START] Preparing the project for Heroku deployment....."

            # Installs psycopg2 and dj-database-url and updates requirements.txt
            pip install psycopg2 dj-database-url
            pip freeze > requirements.txt

            # Updates settings.py with proper heroku database setting
            SETTINGS_PATH="$( find * -name settings.py )"
            echo                                                                                            >> $SETTINGS_PATH
            echo "####"                                                                                     >> $SETTINGS_PATH
            echo "# Heroku Production Server"                                                               >> $SETTINGS_PATH
            echo "# import heroku database settings overriding the defaults"                                >> $SETTINGS_PATH
            echo "# https://devcenter.heroku.com/articles/django#database-settings"                         >> $SETTINGS_PATH
            echo "####"                                                                                     >> $SETTINGS_PATH
            echo "else:"                                                                                    >> $SETTINGS_PATH
            echo "    try:"                                                                                 >> $SETTINGS_PATH
            echo "        import dj_database_url"                                                           >> $SETTINGS_PATH
            echo "        DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}"  >> $SETTINGS_PATH
            echo                                                                                            >> $SETTINGS_PATH
            echo "    except ImportError:"                                                                  >> $SETTINGS_PATH
            echo "        import sys"                                                                       >> $SETTINGS_PATH
            echo "        sys.stderr.write( 'heroku failed to setup database settings\n' )"                 >> $SETTINGS_PATH

            # Commiting for initial heroku deploy
            git add -A && git commit -m "Initial Heroku Deploy preparation complete!"

            echo
            echo "[COMPLETE] Project prepared for Heroku deployment!"
            echo "[START] Creating new Heroku server and deploying....."
            echo

            # Creates a new heroku app with prompted or random name and adds the git remote
            heroku create $HEROKU_NAME

            # Adds a heroku config variable for 'PRODUCTION' and 'DEBUG' so os.environ
            # knows it's a production server and for easy debugging without deploying every time
            heroku config:add PRODUCTION=True
            heroku config:add DEBUG=False

            # Deploys to heroku
            git push heroku master

            # Sync the Django models with the database schema
            heroku run python manage.py syncdb

            # Opens the website in default browser
            echo
            heroku open

            echo
            echo "[COMPLETE] Heroku app deployed and synced!"
            echo
            echo "    # Make sure you also:"
            echo "        - Add any API Secret Keys as config variables"
            echo "        - Migrate any apps on the database"
            echo "        - Configure any custom domains"

        else
            echo "Make sure you're in the top level of the project directory"
        fi

    else
        echo "Make sure to run 'workon PROJECT_NAME'"

    fi
fi
