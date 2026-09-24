# Important: importing models registers them with Base.metadata
from atlas.db import models  # noqa: F401
from atlas.db.database import Base, engine


def main() -> None:
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created.")


if __name__ == "__main__":
    main()
