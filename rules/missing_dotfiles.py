# rules/missing_dotfiles.py

from rules.base import Rule
import os

class MissingDotfiles(Rule):
    name = "Missing Project Dotfiles"
    description = "Checks for the presence of .editorconfig and .gitignore in the root of the repo."

    DEFAULT_CONTENTS = {
        ".editorconfig": """
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
        """.strip(),

        ".gitignore": """
# Python
__pycache__/
*.py[cod]
*.egg
*.egg-info/
dist/
build/
.env
venv/
        """.strip()
    }

    def run(self, repo_path):
        issues = []

        for filename, example_content in self.DEFAULT_CONTENTS.items():
            filepath = os.path.join(repo_path, filename)
            if not os.path.exists(filepath):
                issues.append({
                    "file": filename,
                    "message": f"Missing required file: {filename}",
                    "code": example_content
                })

        if not issues:
            issues.append({
                "message": "✅ All required dotfiles are present."
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }
