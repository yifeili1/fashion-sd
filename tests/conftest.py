"""
Test Configuration for Fashion Design Service
"""
import os
import logging
import pytest
from flask import Flask
from service.models import FashionDesign, db, DataValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')

@pytest.fixture(scope="session")
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    FashionDesign.init_db(app)
    return app

@pytest.fixture(scope="session")
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture(scope="function")
def db_session(app):
    """Create a new database session for a test."""
    with app.app_context():
        # Clean up any existing data
        db.session.query(FashionDesign).delete()
        db.session.commit()
        yield db.session
        db.session.rollback()
        db.session.close()