from . import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Table, DateTime
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime # Import datetime

# Association table for many-to-many relationship between Spreadsheet and User
spreadsheet_users = Table('spreadsheet_users', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('spreadsheet_id', Integer, ForeignKey('spreadsheets.id'), primary_key=True)
)

class DataType(enum.Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"

class Spreadsheet(db.Model):
    __tablename__ = 'spreadsheets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    filename_pattern = Column(String, nullable=True) # New field for filename validation
    rules = relationship("ValidationRule", back_populates="spreadsheet", order_by="ValidationRule.id") # Ordered by ID
    files = relationship("File", back_populates="spreadsheet")
    users = relationship("User", secondary=spreadsheet_users, back_populates="spreadsheets")

class ValidationRule(db.Model):
    __tablename__ = 'validation_rules'
    id = Column(Integer, primary_key=True)
    spreadsheet_id = Column(Integer, ForeignKey('spreadsheets.id'), nullable=False)
    spreadsheet = relationship("Spreadsheet", back_populates="rules")
    column_name = Column(String, nullable=False)
    data_type = Column(Enum(DataType), nullable=False)
    date_format = Column(String)
    required = Column(Boolean, default=True)

def generate_uuid():
    return str(uuid.uuid4())

class File(db.Model):
    __tablename__ = 'files'
    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String, nullable=False)
    spreadsheet_id = Column(Integer, ForeignKey('spreadsheets.id'), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow) # New field
    version = Column(Integer, default=1) # New field
    spreadsheet = relationship("Spreadsheet", back_populates="files")
