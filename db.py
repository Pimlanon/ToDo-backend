from dotenv import load_dotenv
import os
import libsql_client

load_dotenv()

DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# DATABASE_URL = DATABASE_URL.replace("libsql://", "https://")

if not DATABASE_URL or not AUTH_TOKEN:
    raise RuntimeError("Turso environment variables are not set")

_db_client = None

def get_db():
    global _db_client
    if _db_client is None:
        _db_client = libsql_client.create_client_sync(
            url=DATABASE_URL,
            auth_token=AUTH_TOKEN,
        )
    return _db_client