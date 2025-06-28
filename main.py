#!/bin/env python

# main.py

#!/bin/env python

import os
import importlib
import yaml
from rules.base import Rule
from output.formatter import format_as_json, format_as_markdown
from utils.repo_loader import prepare_repo

RULES_DIR = "rules"

def load_config(repo_path):
    config_path = os.path.join(repo_path, ".lintinel.yml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def load_rules():
    rules = []
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".py") and filename != "base.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"{RULES_DIR}.{module_name}")
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, Rule) and obj != Rule:
                    rules.append(obj())
    return rules

def run_lint(repo_url, branch=None, token=None, output_format="json"):
    """
    Clone the repo (with token auth if given), checkout branch,
    run enabled lint rules, and return results formatted as string.
    """
    try:
        repo_path = prepare_repo(repo_url, token=token, branch=branch)
    except Exception as e:
        return f"Error preparing repository: {e}"

    rules = load_rules()
    results = []
    config = load_config(repo_path)
    enabled_rules = config.get("rules", {}) if config else {}

    for rule in rules:
        if enabled_rules and not enabled_rules.get(rule.__class__.__name__, True):
            continue
        try:
            result = rule.run(repo_path)
            if result:
                results.append(result)
        except Exception as e:
            results.append({
                "name": rule.name,
                "description": rule.description,
                "issues": [f"Error running rule: {e}"]
            })

    if results:
        if output_format == "json":
            return format_as_json(results)
        else:
            return format_as_markdown(results)
    else:
        return "No issues found."

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Lintinel - DevOps code auditor")
    parser.add_argument("repo", help="Path to local repo or Git URL")
    parser.add_argument("--branch", help="Git branch to checkout", default=None)
    parser.add_argument("--token", help="GitHub installation token", default=None)
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")
    args = parser.parse_args()

    output = run_lint(args.repo, branch=args.branch, token=args.token, output_format=args.format)
    print(output)

if __name__ == "__main__":
    main()

