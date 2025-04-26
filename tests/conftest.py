import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
import os
from dotenv import load_dotenv
from models.fashion_design import FashionDesign

# Load environment variables
load_dotenv()

# Test database URL
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/fashion_sd_test"
)

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create a fresh database session for each test."""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    
    # Clear all data before each test
    session.query(FashionDesign).delete()
    session.commit()
    
    yield session
    
    # Clean up after test
    session.rollback()
    session.close() 