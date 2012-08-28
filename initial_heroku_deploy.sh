#!/bin/sh
# Kevin Xu / imkevinxu
# 2012.08.28

# Script for initial push to Heroku

# Detects if the user has heroku installed and prompts them to install it if not
if [ -z `which heroku` ]; then

    echo "Detected heroku has not been installed"
    echo "INSTALL heroku here https://devcenter.heroku.com/articles/quickstart"

else

    # Prompts user to make sure he/she is currently working in the virtualenv
    read -p "Are you working in your virtualenv? (Do you see parenthesis on the side?) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then

        # Installs psycopg2 and commits the updated requirements.txt
        pip install psycopg2
        pip freeze > requirements.txt
        git add requirements.txt
        git commit -m "Updated requirements.txt with psycopg2"

        # Creates a new heroku app and adds the git remote
        heroku create

        # Deploys to heroku
        git push heroku master

        # Adds a heroku config variable for 'PRODUCTION' so os.environ knows it's
        # a production server and configures settings accordingly
        heroku config:add PRODUCTION=true

        # Opens the website in default browser
        heroku open

        echo
        echo "    # Make sure to add any custom heroku config variables"
        echo "    # such as API Secret Keys or anything"

    else
        echo "Make sure to run 'workon PROJECT_NAME'"

    fi
fi
