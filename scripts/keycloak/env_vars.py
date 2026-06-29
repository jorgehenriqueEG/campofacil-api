import os

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Get database connection parameters from environment variables
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

keycloak_host = os.getenv("KEYCLOAK_HOST")
keycloak_realm = os.getenv("KEYCLOAK_REALM")
keycloak_admin_user = os.getenv("KEYCLOAK_ADMIN_USER")
keycloak_admin_password = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
