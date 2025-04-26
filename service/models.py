"""
Models for Fashion Design

All of the models are stored in this module
"""
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""

class FashionDesign(db.Model):
    """
    Class that represents a Fashion Design
    """

    app = None

    # Table Schema
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = Column(String, nullable=False)
    negative_prompt = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self):
        """String representation of a FashionDesign"""
        return f"<FashionDesign(id={self.id}, prompt={self.prompt[:50]}...)>"

    def create(self):
        """
        Creates a FashionDesign to the database
        """
        logger.info("Creating %s", self.prompt)
        self.id = str(uuid.uuid4())  # Generate a new UUID
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a FashionDesign to the database
        """
        logger.info("Saving %s", self.prompt)
        db.session.commit()

    def delete(self):
        """Removes a FashionDesign from the data store"""
        logger.info("Deleting %s", self.prompt)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a FashionDesign into a dictionary"""
        return {
            "id": self.id,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "width": self.width,
            "height": self.height,
            "file_path": self.file_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def deserialize(self, data):
        """
        Deserializes a FashionDesign from a dictionary

        Args:
            data (dict): A dictionary containing the FashionDesign data
        """
        try:
            self.prompt = data["prompt"]
            self.negative_prompt = data["negative_prompt"]
            try:
                self.width = int(data["width"])
                self.height = int(data["height"])
            except (ValueError, TypeError):
                raise DataValidationError("Invalid type for integer fields")
            self.file_path = data["file_path"]
        except KeyError as error:
            raise DataValidationError("Invalid FashionDesign: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid FashionDesign: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our SQLAlchemy tables

    @classmethod
    def all(cls):
        """Returns all of the FashionDesigns in the database"""
        logger.info("Processing all FashionDesigns")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a FashionDesign by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_prompt(cls, prompt):
        """Returns all FashionDesigns with the given prompt

        Args:
            prompt (string): the prompt of the FashionDesigns you want to match
        """
        logger.info("Processing prompt query for %s ...", prompt)
        return cls.query.filter(cls.prompt == prompt).all() 