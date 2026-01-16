from dotenv import load_dotenv
import os
import libsql_client

load_dotenv()

print("URL:", os.getenv("TURSO_DATABASE_URL"))
print("TOKEN:", os.getenv("TURSO_AUTH_TOKEN")[:10], "...")

DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

DATABASE_URL = DATABASE_URL.replace("libsql://", "https://")

if not DATABASE_URL or not AUTH_TOKEN:
    raise RuntimeError("Turso environment variables are not set")

def get_db():
    print("Creating DB connection...") 
    client = libsql_client.create_client_sync(
        url=DATABASE_URL,
        auth_token=AUTH_TOKEN,
    )

    print("DB connection established.")
    print(f"Client type: {type(client)}")
    return client