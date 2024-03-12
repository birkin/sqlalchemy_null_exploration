"""
This script will automatically create the database, and tables, defined in the models_sqlalchemy.py file.
I had already created a `DBs` folder at the parent-directory of this .git directory.
"""

from models_sqlalchemy import Base, initialize_engine_session

## ensure the engine and session are initialized
engine = initialize_engine_session()

## create all tables defined in the Base metadata if they don't exist
Base.metadata.create_all(engine)
