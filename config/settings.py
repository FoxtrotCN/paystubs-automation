import os
from dotenv import load_dotenv

load_dotenv()

# API Credentials
API_USER = os.environ.get("API_USER")
API_PASSWORD = os.environ.get("API_PASSWORD")


# Email Service Credentials
FROM_EMAIL = os.environ.get("FROM_EMAIL")
PASSWORD = os.environ.get("EMAIL_PASSWORD")

