"""
Package: service
Package for the application models and service routes
"""
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config.database import SQLALCHEMY_DATABASE_URI
import os

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

# Create static/images directory if it doesn't exist
os.makedirs(os.path.join(app.root_path, 'static', 'images'), exist_ok=True)

# Serve static files
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

def create_app():
    """Create and configure the Flask application"""
    # Initialize database
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True) 