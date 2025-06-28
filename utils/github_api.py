# utils/github_api.py
import requests
from auth import generate_jwt

def get_installation_token(payload):
    installation_id = payload.get("installation", {}).get("id")
    if not installation_id:
        raise Exception("No installation ID in payload")

    jwt_token = generate_jwt()

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }
    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["token"]
