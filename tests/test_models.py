"""
Test cases for Fashion Design Model

Test cases can be run with:
    pytest
    coverage report -m
"""
import os
import logging
import pytest
from service.models import FashionDesign, DataValidationError

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestFashionDesign:
    """Test Cases for FashionDesign Model"""

    @pytest.fixture(autouse=True)
    def setup_class(self, app, db_session):
        """This runs once before the entire test suite"""
        self.app = app
        self.db = db_session

    def test_create_a_fashion_design(self):
        """Test creating a fashion design."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        assert design is not None
        assert design.id is None
        assert design.prompt == "A beautiful dress"
        assert design.negative_prompt == "ugly, deformed"
        assert design.width == 512
        assert design.height == 512
        assert design.file_path == "/path/to/image.png"

    def test_add_a_fashion_design(self):
        """Test adding a fashion design to the database."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        design.create()
        assert design.id is not None

    def test_update_a_fashion_design(self):
        """Test updating a fashion design."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        design.create()
        
        design.prompt = "An elegant dress"
        design.update()
        
        updated = FashionDesign.find(design.id)
        assert updated.prompt == "An elegant dress"

    def test_delete_a_fashion_design(self):
        """Test deleting a fashion design."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        design.create()
        
        design.delete()
        
        deleted = FashionDesign.find(design.id)
        assert deleted is None

    def test_serialize_a_fashion_design(self):
        """Test serializing a fashion design."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        design.create()
        
        data = design.serialize()
        assert data["id"] == design.id
        assert data["prompt"] == "A beautiful dress"
        assert data["negative_prompt"] == "ugly, deformed"
        assert data["width"] == 512
        assert data["height"] == 512
        assert data["file_path"] == "/path/to/image.png"
        assert "created_at" in data

    def test_deserialize_a_fashion_design(self):
        """Test deserializing a fashion design."""
        data = {
            "prompt": "A beautiful dress",
            "negative_prompt": "ugly, deformed",
            "width": 512,
            "height": 512,
            "file_path": "/path/to/image.png"
        }
        design = FashionDesign()
        design.deserialize(data)
        assert design.prompt == "A beautiful dress"
        assert design.negative_prompt == "ugly, deformed"
        assert design.width == 512
        assert design.height == 512
        assert design.file_path == "/path/to/image.png"

    def test_deserialize_missing_data(self):
        """Test deserializing a fashion design with missing data."""
        data = {
            "prompt": "A beautiful dress",
            "width": 512,
            "height": 512
        }
        design = FashionDesign()
        with pytest.raises(DataValidationError):
            design.deserialize(data)

    def test_deserialize_bad_data(self):
        """Test deserializing a fashion design with bad data."""
        data = {
            "prompt": "A beautiful dress",
            "negative_prompt": "ugly, deformed",
            "width": "not a number",
            "height": 512,
            "file_path": "/path/to/image.png"
        }
        design = FashionDesign()
        with pytest.raises(DataValidationError):
            design.deserialize(data)

    def test_find_fashion_design(self):
        """Test finding a fashion design by id."""
        design = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image.png"
        )
        design.create()
        
        found = FashionDesign.find(design.id)
        assert found is not None
        assert found.id == design.id
        assert found.prompt == "A beautiful dress"

    def test_find_by_prompt(self):
        """Test finding fashion designs by prompt."""
        design1 = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image1.png"
        )
        design2 = FashionDesign(
            prompt="A beautiful dress",
            negative_prompt="ugly, deformed",
            width=512,
            height=512,
            file_path="/path/to/image2.png"
        )
        design1.create()
        design2.create()
        
        designs = FashionDesign.find_by_prompt("A beautiful dress")
        assert len(designs) == 2
        assert designs[0].id in [design1.id, design2.id]
        assert designs[1].id in [design1.id, design2.id] 