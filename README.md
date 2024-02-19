# webapp

This is a blog application where users can signup and post their articles as blogs

# Setup

## Database Setup

Run an instance of MySQL database server when developing locally and create a `cloud` database. Once installed create a development user `guest` with password `password` and access to `cloud` database. Assuming `root` user is the admin of database server. Grant all privileges to `guest` user.

    CREATE DATABASE IF NOT EXISTS $DB_NAME;
    CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
    GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
    FLUSH PRIVILEGES;

## Python setup

This is a Flask application. Set up a development environment with

    git clone https://github.com/neucsye6225cloud/webapp.git
    cd webapp
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py


demo changes
