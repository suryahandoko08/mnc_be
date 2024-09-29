import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql://postgres:adminpostgres@localhost/cashflow'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
