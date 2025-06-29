from rules.base import Rule
import os
import subprocess

class YAMLLinter(Rule):
    name = "YAML Linter"
    description = "Checks YAML files for syntax and style issues using yamllint."

    def run(self, repo_path):
        issues = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)

                    try:
                        result = subprocess.run(
                            ["yamllint", "-f", "parsable", file_path],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        if result.stdout:
                            lines = open(file_path).readlines()

                            for line in result.stdout.strip().split("\n"):
                                try:
                                    # Example: path/to/file.yaml:4:5: [error] syntax error: expected <block end>, but found '?'
                                    parts = line.split(":", 3)
                                    if len(parts) == 4:
                                        _, lineno, col, msg = parts
                                        lineno = int(lineno)
                                        start = max(0, lineno - 3)
                                        end = min(len(lines), lineno + 2)
                                        code_block = "".join(lines[start:end]).strip()

                                        issues.append({
                                            "file": rel_path,
                                            "line": lineno,
                                            "message": msg.strip(),
                                            "code": code_block
                                        })
                                except Exception as parse_err:
                                    issues.append({
                                        "file": rel_path,
                                        "message": f"Failed to parse yamllint output: {line}",
                                        "code": ""
                                    })

                    except Exception as e:
                        issues.append({
                            "file": rel_path,
                            "message": f"Failed to run yamllint: {e}",
                            "code": ""
                        })

        if not issues:
            issues.append({
                "message": "✅ No YAML issues found."
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }
