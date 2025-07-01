import unittest
import tempfile
import os
from rules.bash_linter import BashLinter

class TestBashLinter(unittest.TestCase):

    def test_detects_shellcheck_issues(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a bad Bash script
            bad_script = os.path.join(temp_dir, "test.sh")
            with open(bad_script, "w") as f:
                f.write('#!/bin/bash\n')
                f.write('if [ "$foo" = "bar" ]\n')  # Missing 'then'
                f.write('  echo "broken"\n')
                f.write('fi\n')

            # Run the BashLinter
            linter = BashLinter()
            result = linter.run(temp_dir)

            self.assertIn("issues", result)
            issues = result["issues"]

            self.assertTrue(any("Expected 'then'" in issue["message"] for issue in issues))
            self.assertTrue(any("Couldn't parse this if expression" in issue["message"] for issue in issues))

if __name__ == "__main__":
    unittest.main()
