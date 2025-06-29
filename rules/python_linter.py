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
                "issues": [{
                    "message": "✅ No Python files found."
                }]
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
                        line_no = int(line_no)

                        # Read the line of offending code
                        with open(full_path, "r") as f:
                            lines = f.readlines()
                            offending_code = lines[line_no - 1].strip() if 0 < line_no <= len(lines) else ""

                        issues.append({
                            "file": rel_path,
                            "line": line_no,
                            "column": int(col_no),
                            "message": f"[{code}] {message}",
                            "code": offending_code
                        })
                    except Exception as parse_error:
                        issues.append({
                            "message": f"Could not parse flake8 output: {line}",
                            "code": ""
                        })
            else:
                issues.append({
                    "message": "✅ No issues found."
                })

        except Exception as e:
            issues.append({
                "message": f"Error running flake8: {e}"
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues
        }
