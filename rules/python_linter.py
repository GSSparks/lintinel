from rules.base import Rule
import os
import subprocess
from utils.filter_files import is_file_in_changed_list


class PythonLinter(Rule):
    name = "Python Linter"
    description = "Runs flake8 on Python files to enforce PEP8 and linting rules."

    def run(self, repo_path, changed_files=None):
        issues = []

        python_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if not is_file_in_changed_list(file_path, repo_path, changed_files):
                        continue
                    python_files.append(file_path)

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
                ["flake8", "--ignore=E501", "--format=%(path)s::%(row)d::%(col)d::%(code)s::%(text)s"] + python_files,
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
                            "message": f"Could not parse flake8 output: {line}. Error: {parse_error}",
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
