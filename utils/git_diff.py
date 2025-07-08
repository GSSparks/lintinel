# utils/git_diff.py

import subprocess

def get_changed_files(repo_path, base_ref="origin/main"):
    result = subprocess.run(
        ["git", "diff", "--name-only", base_ref, "--diff-filter=ACMR"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    files = result.stdout.strip().splitlines()
    return set(files)
