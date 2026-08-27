import os


# please use SQLite instead of the MySQL database for test.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"