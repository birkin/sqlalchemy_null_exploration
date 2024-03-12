from models_sqlalchemy import Base, initialize_engine_session

## ensure the engine and session are initialized
engine = initialize_engine_session()

## create all tables defined in the Base metadata if they don't exist
Base.metadata.create_all(engine)
