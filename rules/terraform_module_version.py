from rules.base import Rule
import os
import re

class TerraformModuleVersioning(Rule):
    name = "Terraform Module Versioning"
    description = "Ensures all Terraform modules pin a version."

    module_start_pattern = re.compile(r'(?P<full>module\s+"(?P<name>[^"]+)"\s+{)', re.MULTILINE)

    def run(self, repo_path):
        issues = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".tf"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    try:
                        with open(file_path, "r") as f:
                            lines = f.readlines()
                            content = ''.join(lines)

                        # Track modules using line offset
                        for match in self.module_start_pattern.finditer(content):
                            start_line_idx = content[:match.start()].count('\n')
                            name = match.group('name')
                            block_start = match.start()

                            # Try to get full block using braces
                            brace_count = 0
                            block_lines = []
                            for i, line in enumerate(lines[start_line_idx:], start=start_line_idx):
                                brace_count += line.count("{")
                                brace_count -= line.count("}")
                                block_lines.append(line)
                                if brace_count == 0:
                                    break

                            block = ''.join(block_lines)
                            if 'source' in block and 'version' not in block:
                                issues.append({
                                    "file": rel_path,
                                    "line": start_line_idx + 1,
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
