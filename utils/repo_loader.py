# utils/repo_loader.py
import os
import tempfile
import subprocess

def prepare_repo(path_or_url, token=None, branch=None):
    if os.path.isdir(path_or_url):
        return os.path.abspath(path_or_url)
    else:
        tempdir = tempfile.mkdtemp()
        if token:
            if path_or_url.startswith("https://github.com/"):
                url = path_or_url.replace(
                    "https://github.com/",
                    f"https://x-access-token:{token}@github.com/"
                )
            else:
                url = path_or_url
        else:
            url = path_or_url

        subprocess.run(["git", "clone", url, tempdir], check=True)

        if branch:
            subprocess.run(["git", "checkout", branch], cwd=tempdir, check=True)

        return tempdir
