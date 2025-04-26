import pytest
from models.fashion_design import FashionDesign
from datetime import datetime
import uuid

def test_create_fashion_design(db_session):
    """Test creating a new fashion design record."""
    design = FashionDesign(
        prompt="test prompt",
        negative_prompt="test negative prompt",
        width=512,
        height=1024,
        file_path="/path/to/image.png"
    )
    
    db_session.add(design)
    db_session.commit()
    
    # Verify the record was created
    result = db_session.query(FashionDesign).first()
    assert result is not None
    assert result.prompt == "test prompt"
    assert result.negative_prompt == "test negative prompt"
    assert result.width == 512
    assert result.height == 1024
    assert result.file_path == "/path/to/image.png"
    assert isinstance(result.id, uuid.UUID)
    assert isinstance(result.created_at, datetime)

def test_fashion_design_required_fields(db_session):
    """Test that required fields cannot be null."""
    design = FashionDesign()
    
    with pytest.raises(Exception):
        db_session.add(design)
        db_session.commit()

def test_fashion_design_repr(db_session):
    """Test the string representation of FashionDesign."""
    design = FashionDesign(
        prompt="test prompt",
        negative_prompt="test negative prompt",
        width=512,
        height=1024,
        file_path="/path/to/image.png"
    )
    
    db_session.add(design)
    db_session.commit()
    
    assert "FashionDesign" in repr(design)
    assert "test prompt" in repr(design)

def test_multiple_designs(db_session):
    """Test creating multiple fashion designs."""
    designs = [
        FashionDesign(
            prompt=f"prompt {i}",
            negative_prompt=f"negative prompt {i}",
            width=512,
            height=1024,
            file_path=f"/path/to/image_{i}.png"
        )
        for i in range(3)
    ]
    
    for design in designs:
        db_session.add(design)
    db_session.commit()
    
    results = db_session.query(FashionDesign).all()
    assert len(results) == 3
    assert all(isinstance(design.id, uuid.UUID) for design in results)
    assert all(isinstance(design.created_at, datetime) for design in results) 