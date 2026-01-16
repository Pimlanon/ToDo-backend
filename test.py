from db import client

try:
    result = client.execute("SELECT 1;")
    print("Connected to Turso successfully!")
except Exception as e:
    print("Connection failed:", e)
