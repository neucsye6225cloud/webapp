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

## Packer setup

For Google cloud packer, create an IAM service account.
Provide role of 
enable service usage API, compute engine API for new dev project
Set the Environment Variable GOOGLE_APPLICATION_CREDENTIALS to point to the path of the service account key.

gcloud services enable sourcerepo.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable storage-api.googleapis.com
