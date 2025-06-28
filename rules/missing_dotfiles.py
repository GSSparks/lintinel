# rules/missing_dotfiles.py

from rules.base import Rule
import os

class MissingDotfiles(Rule):
    name = "Missing Project Dotfiles"
    description = "Checks for the presence of .editorconfig and .gitignore in the root of the repo."

    def run(self, repo_path):
        issues = []

        expected_files = [".editorconfig", ".gitignore"]

        for filename in expected_files:
            filepath = os.path.join(repo_path, filename)
            if not os.path.exists(filepath):
                issues.append(f"Missing required file: {filename}")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }

