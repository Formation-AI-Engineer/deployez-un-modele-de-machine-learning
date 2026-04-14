"""Create all tables in the database."""

from db.database import engine
from db.models import Base


def create_tables():
    print(f"Creating tables on: {engine.url}")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
