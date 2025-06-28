# tests/test_yaml_linter.py

import os
import tempfile
from rules.yaml_linter import YAMLLinter

def create_test_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def test_yaml_linter_detects_errors():
    with tempfile.TemporaryDirectory() as repo_dir:
        # Create valid YAML file
        valid_yaml = os.path.join(repo_dir, "valid.yml")
        create_test_file(valid_yaml, "foo: bar\nlist:\n  - item1\n  - item2\n")

        # Create invalid YAML file
        invalid_yaml = os.path.join(repo_dir, "invalid.yaml")
        create_test_file(invalid_yaml, "foo: bar: baz\nbad_indent:\n - item1")

        # Run the linter
        linter = YAMLLinter()
        result = linter.run(repo_dir)

        # Check that at least one issue is reported (from the invalid file)
        assert result["name"] == "YAML Linter"
        assert isinstance(result["issues"], list)
        assert any("invalid.yaml" in issue for issue in result["issues"])

        # Optionally: print issues for debugging
        print("\n".join(result["issues"]))

