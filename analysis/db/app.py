from flask import Flask, Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
import os

'''
Note: for running the app, set up the following
    sudo systemctl start mongod
    source myenv/bin/activate
    export FLASK_APP=/media/datak/inactive/analysis/db/app.py
    export FLASK_RUN_CERT=/media/datak/inactive/analysis/db/server.crt
    export FLASK_RUN_KEY=/media/datak/inactive/analysis/db/server.key

Then run
    flask run --cert=$FLASK_RUN_CERT --key=$FLASK_RUN_KEY &>> flask.log
''' 

# Load environment variables from .env file
load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI_LOCAL")

db_app = Flask(__name__)

# Initialize the database driver
db = MongoClient(mongodb_uri)

# Import the routes
from phase1 import phase1_api
from phase2 import phase2_api   
from phase3 import phase3_api
from danger_zone import danger_zone_api

# Register the blueprint
db_app.register_blueprint(phase1_api, url_prefix='/api/phase1')
db_app.register_blueprint(phase2_api, url_prefix='/api/phase2')
db_app.register_blueprint(phase3_api, url_prefix='/api/phase3')
db_app.register_blueprint(danger_zone_api, url_prefix='/api/danger_zone')
