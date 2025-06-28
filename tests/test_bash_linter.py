# tests/test_bash_linter.py

import os
import tempfile
from rules.bash_linter import BashLinter

def test_bash_linter_detects_issues():
    bad_bash_script = """
#!/bin/bash
echo Hello World
VAR=test
if [ "$VAR" = test ] ; then
    echo $VAR
fi
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "bad_script.sh")
        with open(script_path, "w") as f:
            f.write(bad_bash_script)

        rule = BashLinter()
        result = rule.run(tmpdir)

        assert result["issues"], "Expected issues from shellcheck, but got none."
        assert any("bad_script.sh" in issue for issue in result["issues"]), "Script name not found in issue list"
