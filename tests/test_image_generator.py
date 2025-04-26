"""
Tests for the image generator module.
"""
import os
import pytest
from service.image_generator import ImageGenerator
import requests

@pytest.fixture
def image_generator(tmp_path):
    """Create an image generator with a temporary output directory."""
    return ImageGenerator(output_dir=str(tmp_path))

def test_image_generator_initialization(image_generator, tmp_path):
    """Test that the image generator initializes correctly."""
    assert image_generator.webui_url == "http://127.0.0.1:7860"
    assert image_generator.output_dir == str(tmp_path)
    assert os.path.exists(tmp_path)

def test_generate_image_success(image_generator, monkeypatch):
    """Test successful image generation."""
    # Mock the requests.post method
    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return {"images": ["base64_encoded_image_data"]}
        return MockResponse()
    
    monkeypatch.setattr("requests.post", mock_post)
    
    # Mock the base64.b64decode method
    def mock_b64decode(*args, **kwargs):
        return b"fake_image_data"
    monkeypatch.setattr("base64.b64decode", mock_b64decode)
    
    # Test image generation
    filepath = image_generator.generate_image(
        prompt="test prompt",
        negative_prompt="test negative prompt",
        width=512,
        height=1024,
        steps=20
    )
    
    assert os.path.exists(filepath)
    assert filepath.endswith(".png")
    assert os.path.getsize(filepath) > 0

def test_generate_image_request_error(image_generator, monkeypatch):
    """Test handling of request errors."""
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Connection error")
    
    monkeypatch.setattr("requests.post", mock_post)
    
    with pytest.raises(Exception) as exc_info:
        image_generator.generate_image("test prompt")
    assert "Failed to generate image" in str(exc_info.value)

def test_generate_image_invalid_response(image_generator, monkeypatch):
    """Test handling of invalid response from web UI."""
    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return {"invalid": "response"}
        return MockResponse()
    
    monkeypatch.setattr("requests.post", mock_post)
    
    with pytest.raises(Exception) as exc_info:
        image_generator.generate_image("test prompt")
    assert "Error during image generation" in str(exc_info.value) 