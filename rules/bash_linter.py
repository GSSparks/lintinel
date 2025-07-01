from rules.base import Rule
import os
import subprocess
import json

class BashLinter(Rule):
    name = "Bash Linter"
    description = "Checks .sh files for syntax and style issues using shellcheck."

    def run(self, repo_path):
        issues = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".sh"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)

                    try:
                        with open(file_path, "r") as f:
                            lines = f.readlines()

                        result = subprocess.run(
                            ["shellcheck", "--format", "json", file_path],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        diagnostics = json.loads(result.stdout)

                        # If it's a list, iterate directly
                        if isinstance(diagnostics, list):
                            comments = diagnostics
                        else:
                            comments = diagnostics.get("comments", [])

                        for comment in comments:
                            line_no = comment.get("line", 0)
                            message = comment.get("message", "Unknown issue")
                            code_line = lines[line_no - 1].strip() if 0 < line_no <= len(lines) else ""

                            issues.append({
                                "file": rel_path,
                                "line": line_no,
                                "message": message,
                                "code": code_line
                            })

                    except Exception as e:
                        issues.append({
                            "file": rel_path,
                            "message": f"Failed to run shellcheck: {e}",
                            "code": ""
                        })

        if not issues:
            issues.append({
                "message": "✅ No Bash issues found."
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues
        }
