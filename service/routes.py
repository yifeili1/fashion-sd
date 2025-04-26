"""
Fashion Design Service Routes

This module implements the RESTful API endpoints for the Fashion Design service.
"""

from flask import Blueprint, jsonify, request
from service.models import db, FashionDesign
from service.image_generator import ImageGenerator

# Create a Blueprint for the fashion design routes
fashion_design_bp = Blueprint('fashion_design', __name__)

# Initialize the image generator
image_generator = ImageGenerator()

@fashion_design_bp.route('/designs', methods=['GET'])
def list_designs():
    """List all fashion designs."""
    designs = FashionDesign.query.all()
    return jsonify([design.serialize() for design in designs])

@fashion_design_bp.route('/designs', methods=['POST'])
def create_design():
    """Create a new fashion design."""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        # Generate the image
        file_path = image_generator.generate_image(
            prompt=data['prompt'],
            negative_prompt=data.get('negative_prompt', ''),
            width=data.get('width', 512),
            height=data.get('height', 512)
        )
        
        # Create new design
        design = FashionDesign(
            prompt=data['prompt'],
            negative_prompt=data.get('negative_prompt', ''),
            width=data.get('width', 512),
            height=data.get('height', 512),
            file_path=file_path
        )
        
        db.session.add(design)
        db.session.commit()
        return jsonify(design.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fashion_design_bp.route('/designs/<string:design_id>', methods=['GET'])
def get_design(design_id):
    """Get a specific fashion design by ID."""
    design = FashionDesign.query.get(design_id)
    if not design:
        return jsonify({'error': 'Design not found'}), 404
    return jsonify(design.serialize())

@fashion_design_bp.route('/designs/<string:design_id>', methods=['DELETE'])
def delete_design(design_id):
    """Delete a specific fashion design."""
    design = FashionDesign.query.get(design_id)
    if not design:
        return jsonify({'error': 'Design not found'}), 404
    
    try:
        db.session.delete(design)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@fashion_design_bp.route('/designs/search', methods=['GET'])
def search_designs():
    """Search designs by prompt."""
    prompt = request.args.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'Search prompt is required'}), 400
    
    designs = FashionDesign.query.filter(
        FashionDesign.prompt.ilike(f'%{prompt}%')
    ).all()
    
    return jsonify([design.serialize() for design in designs]) 