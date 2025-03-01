# backend/api/__init__.py
import sys
import os
from flask import Flask
from flask import Blueprint
from backend import database
from backend.models import db, init_db
from frontend.components import cve_table


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Initialize Blueprint for API routes

app = Flask(__name__)
api_bp = Blueprint("api", __name__)

# Import routes to register them with the blueprint
from backend.api import filter_routes, other_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cve_database.db'
    init_db(app)

    # Register Blueprints
    app.register_blueprint(cve_table, url_prefix="/api")

    return app

