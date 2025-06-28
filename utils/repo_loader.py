# utils/repo_loader.py
import os
import tempfile
import subprocess

def prepare_repo(path_or_url):
    if os.path.isdir(path_or_url):
        return os.path.abspath(path_or_url)
    else:
        tempdir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", path_or_url, tempdir], check=True)
        return tempdir

