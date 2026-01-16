from dotenv import load_dotenv
import os
import libsql_client

load_dotenv()

print("URL:", os.getenv("TURSO_DATABASE_URL"))
print("TOKEN:", os.getenv("TURSO_AUTH_TOKEN")[:10], "...")

DATABASE_URL = os.getenv("TURSO_DATABASE_URL").replace("libsql://", "https://")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

client = libsql_client.create_client_sync(
    url=DATABASE_URL,
    auth_token=AUTH_TOKEN,
)
