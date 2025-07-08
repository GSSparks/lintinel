from rules.base import Rule
import os
from utils.filter_files import is_file_in_changed_list



class MissingDotfiles(Rule):
    name = "Missing Project Dotfiles"
    description = "Checks for the presence of .editorconfig and .gitignore in the root of the repo."

    DEFAULT_CONTENTS = {
        ".editorconfig": "#",
        ".gitignore": "#"
    }

    def run(self, repo_path, changed_files=None):
        issues = []

        for filename, example_content in self.DEFAULT_CONTENTS.items():
            filepath = os.path.join(repo_path, filename)

            # If running in PR-only mode and the file is not in the diff, skip it
            if changed_files is not None and not is_file_in_changed_list(filepath, repo_path, changed_files):
                continue

            if not os.path.exists(filepath):
                issues.append({
                    "file": filename,
                    "message": f"Missing required file: {filename}",
                    "code": example_content
                })

        if not issues:
            # If we're checking only PR files, don't report "✅ All clear"
            if changed_files is None:
                issues.append({
                    "message": "✅ All required dotfiles are present."
                })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }
