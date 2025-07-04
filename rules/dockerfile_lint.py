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
                    rel_path = os.path.relpath(dockerfile_path, repo_path)

                    try:
                        dfp = DockerfileParser(path=dockerfile_path)
                        base_image = dfp.baseimage

                        if base_image and (":" not in base_image or base_image.endswith(":latest")):
                            with open(dockerfile_path) as f:
                                lines = f.readlines()
                            for idx, line in enumerate(lines):
                                if line.strip().startswith("FROM"):
                                    issues.append({
                                        "file": rel_path,
                                        "line": idx + 1,
                                        "message": f"Base image '{base_image}' is not pinned to a specific version.",
                                        "code": line.strip()
                                    })
                                    break

                    except Exception as e:
                        issues.append({
                            "file": rel_path,
                            "message": f"❌ Failed to parse Dockerfile: {e}",
                            "code": ""
                        })

        if not issues:
            issues.append({
                "message": "✅ No Dockerfile issues found."
            })

        return {
            "name": self.name,
            "description": self.description,
            "issues": issues
        }
