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
                    rel_path = os.path.relpath(file_path, repo_path)
                    try:
                        result = subprocess.run(
                            ["shellcheck", "-f", "gcc", file_path],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        # Example line: script.sh:5:1: warning: Use `#!/usr/bin/env bash` instead of `#!/bin/bash`
                        for line in result.stdout.strip().split("\n"):
                            try:
                                parts = line.split(":", 3)
                                if len(parts) == 4:
                                    _, line_no, col_no, message = parts
                                    line_no = int(line_no)
                                    col_no = int(col_no)

                                    with open(file_path, "r") as f:
                                        lines = f.readlines()
                                        code = lines[line_no - 1].strip() if 0 < line_no <= len(lines) else ""

                                    issues.append({
                                        "file": rel_path,
                                        "line": line_no,
                                        "column": col_no,
                                        "message": message.strip(),
                                        "code": code
                                    })
                            except Exception as parse_err:
                                issues.append({
                                    "file": rel_path,
                                    "message": f"Failed to parse shellcheck output: {line}",
                                    "code": ""
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
