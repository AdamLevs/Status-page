import secrets
import os

# Basic configuration for a status page DB and Redis setup
POSTGRES_USER = "Admin"
POSTGRES_PASSWORD = "Password"
POSTGRES_DB = "statuspage"
REDIS_URL = "redis://redis:6379/0"

# Generate a random secret key for the application
SECRET_KEY = secrets.token_urlsafe(32)

# Write the configuration to a .env file
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
with open(env_path, "w") as f:
    f.write(f"POSTGRES_USER={POSTGRES_USER}\n")
    f.write(f"POSTGRES_PASSWORD={POSTGRES_PASSWORD}\n")
    f.write(f"POSTGRES_DB={POSTGRES_DB}\n")
    f.write(f"REDIS_URL={REDIS_URL}\n")
    f.write(f"SECRET_KEY={SECRET_KEY}\n")


print("✅ .env file generated successfully:")
print(f"POSTGRES_USER={POSTGRES_USER}")
print(f"POSTGRES_PASSWORD={POSTGRES_PASSWORD}")
print(f"POSTGRES_DB={POSTGRES_DB}")
print(f"REDIS_URL={REDIS_URL}")
print(f"SECRET_KEY={SECRET_KEY}")
