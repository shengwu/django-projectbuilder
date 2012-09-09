#!/bin/sh
# Kevin Xu / imkevinxu
# 2012.08.28
#
# Script for initial deploy to Heroku
# Tested on Mac 10.7 Lion
#####################################

# Script that undos the work of the initial heroku deployment littered with emoticans
# Invoked by an --undo parameter
#
# UNINSTALLS 'psycopg2' and 'dj-database-url',
# RESETS the git head back one commit, and
# DESTROYS the heroku app
#####################################
if [ ! -d $1 ]; then
    if [ $1 == "--undo" ]; then
        echo
        echo "    Sounds like something broke during the initial deployment......"
        echo
        echo "    (╯°□°）╯︵ ┻━┻    FFFFFFFUUUUUUUUUUUU"
        echo
        read -p "    Are you sure you wish to undo the initial deploy? " -n 1
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo
            echo "    （╯ ﾟ ヮﾟ）╯︵ ♥♥♥♥  i love you!"
            exit 0
        fi
        echo
        echo "    This will UNINSTALL 'psycopg2' and 'dj-database-url',"
        echo "    RESET the git head back one commit, and DESTROY the heroku app"
        read -p "    Last chance, are you sure you want to undo? " -n 1
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo
            echo "    ┬──┬﻿ ノ( ゜-゜ノ)  chill out bro"
            exit 0
        fi

        echo
        echo "    ┻━┻ ︵ヽ(\`Д´)ﾉ︵* ┻━┻    RAAAAAAAAAGEEEEEEEE!!!!!"
        echo
        read -p "    What is the name of the Heroku app? "
        echo
        echo "[START] Undoing initial Heroku deployment....."
        pip uninstall psycopg2 dj-database-url
        git reset --hard HEAD^
        heroku destroy --app $REPLY
        echo
        echo "[COMPLETE] Initial Heroku deployment successfully undone!"
        echo
        echo "    (^_^メ) That wasn't too bad..."

        exit 0
    else
        echo "[EXTRA ARGUMENTS] Script takes no extra arguments"
        exit 0
    fi
fi

# Detects if the user has heroku installed and prompts them to install it if not
if [ -z `which heroku` ]; then
    echo "[MISSING HEROKU] Detected Heroku has not been installed"
    echo "  INSTALL Heroku here https://devcenter.heroku.com/articles/quickstart"
    exit 0
fi

# Proceed if user is working in a virtualenv
if [ ! -d "$VIRTUAL_ENV" ]; then
    echo "[MISSING VIRTUALEV] Not currently working in the project's virtualenv"
    echo "  run 'workon PROJECT_NAME'"
    exit 0
fi

# Proceed if user is currently in the top level directory of the project
if [ ! -s "manage.py" ]; then
    echo "[WRONG FOLDER] You're not in the top level of the project directory"
    echo "  Only run script in the same folder as 'manage.py' of the project"
    exit 0
fi

# Proceed if user is currently in the master branch
branch_name=$(git symbolic-ref HEAD 2>/dev/null)
branch_name=${branch_name##refs/heads/}
if [ $branch_name != "master" ]; then
    echo "[WRONG BRANCH] You currently have the '$branch_name' git branch checked out"
    echo "  Please check out the 'master' branch and make any updates/merges"
    exit 0
fi


# Begin Deployment Script
echo
echo "    *** Starting Initial Heroku Deploy! ***"
echo
echo "      　　　　 /｀》,-―‐‐＜｀}           "
echo "      　　 　./::/≠´::::;::ヽ.           "
echo "      　 　　/::〃::::／}::丿ハ          "
echo "      　 　./:::i{::／  ﾉ／}::}          "
echo "      　　 /::::瓜イ＞ ´＜,':ﾉ           "
echo "      　 ./::::ﾉ ﾍ{､ ( ﾌ_ノイ            "
echo "      　 |::::|  ／} ｽ/￣￣￣￣/         "
echo "       　|::::| (::つ/ Heroku / Deploy!  "
echo "    ￣￣￣￣￣￣￣＼/＿＿＿＿/￣￣￣￣   "
echo

# Prompts user for a name of the heroku app
read -p "    What will you name the new Heroku app? (single word lowercase. leave blank for random name) "
HEROKU_NAME=$REPLY

echo
echo "[START] Preparing the project for Heroku deployment....."

# Installs psycopg2 and dj-database-url and updates requirements.txt
env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
pip install dj-database-url
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

echo "[COMPLETE] Heroku app deployed and synced!"
echo
echo "    ヽ(^o^)丿  yaaaaaaaay"
echo
echo "    # Make sure you also:"
echo "        - Add any API Secret Keys as config variables"
echo "        - Migrate any apps on the database"
echo "        - Configure any custom domains"
echo
echo "    # In case there was an error during deployment, run the script again with --undo parameter"


