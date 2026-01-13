import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/spreadsheet_validator'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
