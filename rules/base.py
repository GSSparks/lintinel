# rules/base.py

class Rule:
    name = "Unnamed Rule"
    description = "No description provided"

    def run(self, repo_path):
        """Override this to implement rule logic"""
        raise NotImplementedError
