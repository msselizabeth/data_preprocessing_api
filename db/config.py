import os
from pathlib import Path

default_database_path = Path(__file__).resolve().parent / "database_prod.db"

database_path = Path(
    os.environ.get("DATABASE_PATH", str(default_database_path))
).expanduser().resolve()

database_url = f"sqlite+aiosqlite:///{database_path}"