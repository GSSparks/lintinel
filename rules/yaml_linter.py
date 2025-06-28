# rules/yaml_linter.py

from rules.base import Rule
import os
import subprocess

class YAMLLinter(Rule):
    name = "YAML Linter"
    description = "Checks YAML files for syntax and style issues using yamllint."

    def run(self, repo_path):
        issues = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    file_path = os.path.join(root, file)
                    try:
                        result = subprocess.run(
                            ["yamllint", "-f", "parsable", file_path],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        if result.stdout:
                            for line in result.stdout.strip().split("\n"):
                                issues.append(f"{file_path}: {line}")

                    except Exception as e:
                        issues.append(f"{file_path}: Failed to run yamllint ({e})")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }

