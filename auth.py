import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

APP_ID = int(os.getenv("GITHUB_APP_ID"))
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

def generate_jwt():
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + (10 * 60),  # max 10 minutes
        "iss": APP_ID
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
