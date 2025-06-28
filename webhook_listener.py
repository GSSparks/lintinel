#!/bin/env python

# webhook-listener.py

from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import os
import json
import requests

from main import run_lint
from utils.github_api import get_installation_token

app = FastAPI()

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")


def verify_signature(secret, payload, signature_header):
    if not signature_header:
        return False
    try:
        sha_name, signature = signature_header.split("=")
    except ValueError:
        return False
    if sha_name != "sha256":
        return False
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


def post_pr_comment(token, repo_full_name, issue_number, body):
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": body}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()


@app.post("/webhook")
async def github_webhook(request: Request,
                         x_hub_signature_256: str = Header(None),
                         x_github_event: str = Header(None)):
    raw_body = await request.body()

    if not verify_signature(GITHUB_SECRET, raw_body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event_type = x_github_event

    if event_type == "ping":
        print("✅ Received ping from GitHub")
        return {"msg": "pong"}

    if event_type == "pull_request":
        action = payload.get("action")
        if action in ["opened", "reopened", "synchronize"]:
            pr = payload.get("pull_request")
            repo_full_name = payload.get("repository", {}).get("full_name")
            branch = pr.get("head", {}).get("ref")
            sha = pr.get("head", {}).get("sha")
            issue_number = pr.get("number")

            print(f"📦 PR event: {action} on {repo_full_name}@{branch} ({sha})")

            # Step 1: Authenticate as GitHub App & get installation token
            # (You'll need your own function to do this - here’s a stub)
            try:
                install_token = get_installation_token(payload)
            except Exception as e:
                print(f"❌ Failed to get installation token: {e}")
                raise HTTPException(status_code=500, detail="Failed to authenticate with GitHub")

            # Step 2: Run lint using main.py function
            lint_output = run_lint(
                repo_url=f"https://github.com/{repo_full_name}.git",
                branch=branch,
                token=install_token,
                output_format="markdown"
            )

            # Step 3: Post comment back to PR
            try:
                post_pr_comment(install_token, repo_full_name, issue_number, lint_output)
                print(f"💬 Posted lint results comment to PR #{issue_number}")
            except Exception as e:
                print(f"❌ Failed to post PR comment: {e}")

    return {"status": "ok"}
