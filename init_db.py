"""Create an empty local database. Existing files are never replaced."""
import argparse
import os
from pathlib import Path
import sqlite3


def initialize(path):
    path = Path(path)
    # Exclusive creation avoids overwriting a database even in concurrent invocations.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        with sqlite3.connect(path) as connection:
            connection.executescript(Path(__file__).with_name("schema.sql").read_text())
    except Exception:
        path.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=os.environ.get("TRIVIA_DATABASE", "triviaTrials.db"))
    args = parser.parse_args()
    try:
        initialize(args.path)
    except FileExistsError:
        parser.error("Database already exists; choose a new path.")
    print("Created an empty local database. Register through the app to begin.")
