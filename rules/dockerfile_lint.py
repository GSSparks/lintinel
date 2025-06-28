# rules/dockerfile_lint.py

from rules.base import Rule
import os
from dockerfile_parse import DockerfileParser

class DockerfileBestPractices(Rule):
    name = "Dockerfile Best Practices"
    description = "Checks for unpinned base images in Dockerfiles (e.g., 'ubuntu:latest')"

    def run(self, repo_path):
        issues = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file == "Dockerfile":
                    dockerfile_path = os.path.join(root, file)
                    try:
                        with open(dockerfile_path, "r") as f:
                            content = f.read()

                        dfp = DockerfileParser()
                        dfp.content = content
                        base_image = dfp.baseimage

                        if base_image:
                            if ":" not in base_image or base_image.endswith(":latest"):
                                issues.append(
                                    f"{dockerfile_path}: Base image '{base_image}' is not pinned to a specific version."
                                )
                    except Exception as e:
                        issues.append(f"{dockerfile_path}: Failed to parse Dockerfile ({e})")

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues,
        }

