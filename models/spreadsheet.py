from . import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import uuid

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
    rules = relationship("ValidationRule", back_populates="spreadsheet")
    files = relationship("File", back_populates="spreadsheet")

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
    spreadsheet = relationship("Spreadsheet", back_populates="files")
