# rules/terraform_module_versioning.py

from rules.base import Rule
import os
import re

class TerraformModuleVersioning(Rule):
    name = "Terraform Module Versioning"
    description = "Ensures all Terraform modules pin a version."

    module_start_pattern = re.compile(r'(?P<full>module\s+"(?P<name>[^"]+)"\s+{)', re.MULTILINE)

    def run(self, repo_path):
        issues = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".tf"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()

                        # Find each module block by regex match
                        for match in self.module_start_pattern.finditer(content):
                            name = match.group("name")
                            block_start = match.start()
                            remaining = content[block_start:]

                            # Parse block using brace counting
                            brace_count = 0
                            block_chars = []
                            for idx, char in enumerate(remaining):
                                block_chars.append(char)
                                if char == "{":
                                    brace_count += 1
                                elif char == "}":
                                    brace_count -= 1
                                    if brace_count == 0:
                                        break

                            block = "".join(block_chars)
                            block_lines = content[:block_start + len(block)].splitlines()
                            line_offset = content[:block_start].count('\n')

                            if 'source' in block and 'version' not in block:
                                issues.append({
                                    "file": rel_path,
                                    "line": line_offset + 1,
                                    "message": f"Module '{name}' has no pinned version.",
                                    "code": block.strip()
                                })

                    except Exception as e:
                        issues.append({
                            "file": rel_path,
                            "message": f"Failed to scan Terraform file: {e}",
                            "code": ""
                        })

        if not issues:
            issues.append({
                "message": "✅ All Terraform modules are pinned to a version."
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }
