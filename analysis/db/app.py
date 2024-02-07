from flask import Flask, Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")

app = Flask(__name__)

# Initialize the database driver
db = MongoClient(mongodb_uri)

# Import the routes
from phase1 import phase1_api
from phase2 import phase2_api   
from phase3 import phase3_api
from danger_zone import danger_zone_api

# Register the blueprint
app.register_blueprint(phase1_api, url_prefix='/api/phase1')
app.register_blueprint(phase2_api, url_prefix='/api/phase2')
app.register_blueprint(phase3_api, url_prefix='/api/phase3')
app.register_blueprint(danger_zone_api, url_prefix='/api/danger_zone')
