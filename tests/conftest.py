"""
Test configuration for the Fashion Design Service.
"""
import os
import logging
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from service.models import FashionDesign, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
SQLITE_DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture(scope="session")
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the test app
    db.init_app(app)
    
    # Register blueprints
    from service.routes import fashion_design_bp
    app.register_blueprint(fashion_design_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture(scope="function")
def test_db(app):
    """Create a test database."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()