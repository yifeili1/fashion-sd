"""
Package: service
Package for the application models and service routes
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.database import SQLALCHEMY_DATABASE_URI

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes after app initialization to avoid circular imports
from service.routes import fashion_design_bp

# Register blueprints
app.register_blueprint(fashion_design_bp)

def create_app():
    """Create and configure the Flask application"""
    # Initialize database
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True) 