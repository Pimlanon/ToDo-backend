from dotenv import load_dotenv
import os
import libsql_client

load_dotenv()

DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if not DATABASE_URL or not AUTH_TOKEN:
    raise RuntimeError("Turso environment variables are not set")

client = libsql_client.create_client_sync(
    url=DATABASE_URL,
    auth_token=AUTH_TOKEN,
)

def get_db():
    return client