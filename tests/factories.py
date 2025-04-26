"""
Test Factory for Fashion Design Service
"""
import uuid
from datetime import datetime
from service.models import FashionDesign

def create_fashion_design(prompt="test prompt", negative_prompt="test negative prompt",
                        width=512, height=512, file_path="test/path/image.png"):
    """Creates a fake fashion design for testing"""
    return FashionDesign(
        id=uuid.uuid4(),
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        file_path=file_path,
        created_at=datetime.utcnow()
    ) 