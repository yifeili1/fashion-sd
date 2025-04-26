"""
Test cases for the Fashion Design Service routes.
"""

import pytest
from flask_sqlalchemy import SQLAlchemy
from service.models import FashionDesign
from service.routes import fashion_design_bp

@pytest.fixture
def app():
    """Create a Flask app for testing."""
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy
    db = SQLAlchemy(app)
    
    # Register the blueprint
    app.register_blueprint(fashion_design_bp)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_design(app):
    """Create a sample fashion design for testing."""
    with app.app_context():
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, blurry",
            width=512,
            height=512,
            file_path="/path/to/image.jpg"
        )
        db.session.add(design)
        db.session.commit()
        return design

@pytest.fixture(autouse=True)
def setup_test_db(test_db, app):
    """Set up test database."""
    with app.app_context():
        test_db.session.query(FashionDesign).delete()
        test_db.session.commit()

def test_list_designs_empty(client):
    """Test listing designs when database is empty."""
    response = client.get('/designs')
    assert response.status_code == 200
    assert response.json == []

def test_list_designs(client, test_db, app):
    """Test listing designs when database has data."""
    with app.app_context():
        design = FashionDesign(
            prompt="Test design",
            negative_prompt="bad quality",
            width=512,
            height=512,
            file_path="/path/to/image.jpg"
        )
        test_db.session.add(design)
        test_db.session.commit()

        response = client.get('/designs')
        assert response.status_code == 200
        designs = response.json
        assert len(designs) == 1
        assert designs[0]['prompt'] == "Test design"

def test_create_design(client):
    """Test creating a new design."""
    data = {
        'prompt': 'New design',
        'negative_prompt': 'bad quality',
        'width': 512,
        'height': 512,
        'file_path': '/path/to/image.jpg'
    }
    response = client.post('/designs', json=data)
    assert response.status_code == 201
    assert response.json['prompt'] == 'New design'

def test_create_design_missing_prompt(client):
    """Test creating a design without required fields."""
    data = {
        'negative_prompt': 'bad quality',
        'width': 512,
        'height': 512
    }
    response = client.post('/designs', json=data)
    assert response.status_code == 400

def test_get_design(client, test_db, app):
    """Test getting a specific design."""
    with app.app_context():
        design = FashionDesign(
            prompt="Test design",
            negative_prompt="bad quality",
            width=512,
            height=512,
            file_path="/path/to/image.jpg"
        )
        test_db.session.add(design)
        test_db.session.commit()

        response = client.get(f'/designs/{design.id}')
        assert response.status_code == 200
        assert response.json['prompt'] == "Test design"

def test_get_nonexistent_design(client):
    """Test getting a design that doesn't exist."""
    response = client.get('/designs/999')
    assert response.status_code == 404

def test_delete_design(client, test_db, app):
    """Test deleting a design."""
    with app.app_context():
        design = FashionDesign(
            prompt="Test design",
            negative_prompt="bad quality",
            width=512,
            height=512,
            file_path="/path/to/image.jpg"
        )
        test_db.session.add(design)
        test_db.session.commit()

        response = client.delete(f'/designs/{design.id}')
        assert response.status_code == 204

def test_delete_nonexistent_design(client):
    """Test deleting a design that doesn't exist."""
    response = client.delete('/designs/999')
    assert response.status_code == 404

def test_search_designs(client, test_db, app):
    """Test searching designs with results."""
    with app.app_context():
        design = FashionDesign(
            prompt="Beautiful dress",
            negative_prompt="bad quality",
            width=512,
            height=512,
            file_path="/path/to/image.jpg"
        )
        test_db.session.add(design)
        test_db.session.commit()

        response = client.get('/designs/search?prompt=dress')
        assert response.status_code == 200
        designs = response.json
        assert len(designs) == 1
        assert designs[0]['prompt'] == "Beautiful dress"

def test_search_designs_empty(client):
    """Test searching designs with no results."""
    response = client.get('/designs/search?prompt=nonexistent')
    assert response.status_code == 200
    assert response.json == []

def test_search_designs_missing_prompt(client):
    """Test searching designs without a prompt."""
    response = client.get('/designs/search')
    assert response.status_code == 400 