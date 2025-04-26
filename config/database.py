"""
Database configuration for Fashion Design Service
"""
import os

# Get database URL from environment variable or use SQLite as default
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "sqlite:///fashion_design.db"
) 