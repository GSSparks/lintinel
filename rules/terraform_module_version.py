# rules/terraform_module_version.py

from rules.base import Rule
import os
import re

class TerraformModuleVersioning(Rule):
    name = "Terraform Module Versioning"
    description = "Ensures all Terraform modules pin a version."

    def run(self, repo_path):
        issues = []
        module_block_pattern = re.compile(r'module\s+"([^"]+)"\s+{([^}]+)}', re.MULTILINE | re.DOTALL)
        version_pattern = re.compile(r'version\s*=\s*"[^"]+"')

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".tf"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()

                        modules = module_block_pattern.findall(content)
                        for module_name, block_content in modules:
                            if 'source' in block_content and 'version' not in block_content:
                                issues.append(
                                    f"{file_path}: Module '{module_name}' has no pinned version."
                                )

                    except Exception as e:
                        issues.append(f"{file_path}: Failed to scan Terraform file ({e})")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }

