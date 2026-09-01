from src.config.database import Base, engine


# Create database tables.
# In normal use, this creates the tables in MySQL.
Base.metadata.create_all(bind=engine)