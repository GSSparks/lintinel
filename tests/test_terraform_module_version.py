# tests/test_terraform_module_version.py

import os
import tempfile
from rules.terraform_module_version import TerraformModuleVersioning

def create_test_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def test_terraform_module_versioning_detects_unpinned_modules():
    with tempfile.TemporaryDirectory() as repo_dir:
        # Good module (has version)
        good_tf = os.path.join(repo_dir, "main.tf")
        create_test_file(good_tf, '''
        module "vpc" {
          source  = "terraform-aws-modules/vpc/aws"
          version = "3.5.0"
        }
        ''')

        # Bad module (no version)
        bad_tf = os.path.join(repo_dir, "unversioned.tf")
        create_test_file(bad_tf, '''
        module "ec2" {
          source = "terraform-aws-modules/ec2/aws"
        }
        ''')

        rule = TerraformModuleVersioning()
        result = rule.run(repo_dir)

        assert result["name"] == "Terraform Module Versioning"
        assert any("ec2" in issue for issue in result["issues"])
        assert not any("vpc" in issue for issue in result["issues"])

        # Optional: Print for debug
        print("\n".join(result["issues"]))

