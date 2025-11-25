from dotenv import load_dotenv
import os

# Load environment variables from a .env file (if present)
load_dotenv()

# --- Database Configuration ---
# Uses a default connection string if DATABASE_URL is not set in the environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
)

# --- Authentication Configuration ---
# Google OAuth Client ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")

# JWT Secret Key for signing tokens (CRITICAL: Change this default!)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-change-me")

# JWT Access Token expiration time in minutes
ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_EXPIRE_MINUTES", 5))

# JWT Refresh Token expiration time in days
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", 15))

# --- Application Configuration ---
# Frontend Origin URL for CORS configuration
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")