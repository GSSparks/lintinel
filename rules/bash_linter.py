# rules/bash_linter.py

from rules.base import Rule
import os
import subprocess

class BashLinter(Rule):
    name = "Bash Linter"
    description = "Checks .sh files for syntax and style issues using shellcheck"

    def run(self, repo_path):
        issues = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".sh"):
                    file_path = os.path.join(root, file)
                    try:
                        result = subprocess.run(
                            ["shellcheck", file_path],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        if result.stdout.strip():
                            for line in result.stdout.strip().split("\n"):
                                issues.append(f"{file_path}: {line}")

                    except Exception as e:
                        issues.append(f"{file_path}: Failed to run shellcheck ({e})")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }
