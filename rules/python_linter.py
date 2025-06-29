# rules/python_linter.py

from rules.base import Rule
import os
import subprocess

class PythonLinter(Rule):
    name = "Python Linter"
    description = "Runs flake8 on Python files to enforce PEP8 and linting rules."

    def run(self, repo_path):
        issues = []

        python_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        if not python_files:
            return {
                "name": self.name,
                "description": self.description,
                "issues": ["✅ No Python files found."]
            }

        try:
            result = subprocess.run(
                ["flake8", "--format=%(path)s::%(row)d::%(col)d::%(code)s::%(text)s"] + python_files,
                capture_output=True,
                text=True,
                check=False
            )

            if result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    try:
                        full_path, line_no, col_no, code, message = line.split("::", 4)
                        rel_path = os.path.relpath(full_path, repo_path)
                        issues.append(f"{rel_path:<40} Line {line_no}, Col {col_no}  [{code}]  {message}")
                    except ValueError:
                        # If parsing fails, fallback to raw line
                        issues.append(line)
            else:
                issues.append("✅ No issues found.")

        except Exception as e:
            issues.append(f"Error running flake8: {e}")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues
        }
