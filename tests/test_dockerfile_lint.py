# tests/test_dockerfile_lint.py

import os
import tempfile
from rules.dockerfile_lint import DockerfileBestPractices


def create_dockerfile(path, content):
    with open(path, "w") as f:
        f.write(content)


def test_dockerfile_lint_detects_unpinned_base_image():
    with tempfile.TemporaryDirectory() as repo_dir:
        # Dockerfile with unpinned base image
        bad_dockerfile = os.path.join(repo_dir, "Dockerfile")
        create_dockerfile(bad_dockerfile, "FROM ubuntu:latest\nRUN apt-get update")

        rule = DockerfileBestPractices()
        result = rule.run(repo_dir)

        assert result["name"] == "Dockerfile Best Practices"
        assert any("ubuntu:latest" in issue for issue in result["issues"])


def test_dockerfile_lint_ignores_pinned_base_image():
    with tempfile.TemporaryDirectory() as repo_dir:
        # Dockerfile with pinned base image
        good_dockerfile = os.path.join(repo_dir, "Dockerfile")
        create_dockerfile(good_dockerfile, "FROM ubuntu:20.04\nRUN apt-get update")

        rule = DockerfileBestPractices()
        result = rule.run(repo_dir)

        assert result["name"] == "Dockerfile Best Practices"
        assert result["issues"] == []
