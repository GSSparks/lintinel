#!/bin/env python

# main.py

import argparse
import os
import importlib
import json
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

def main():
    parser = argparse.ArgumentParser(description="Lintinel - DevOps code auditor")
    parser.add_argument("repo", help="Path to local repo or Git URL")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")
    args = parser.parse_args()

    try:
        repo_path = prepare_repo(args.repo)
    except Exception as e:
        print(f"Error preparing repository: {e}")
        return

    rules = load_rules()
    results = []
    config = load_config(repo_path)
    enabled_rules = config.get("rules", {}) if config else {}

    for rule in rules:
        if enabled_rules and not enabled_rules.get(rule.__class__.__name__, True):
            continue
        print(f"Running rule: {rule.name}")
        try:
            result = rule.run(repo_path)
            if result:
                results.append(result)
        except Exception as e:
            print(f"Error running rule {rule.name}: {e}")

    if results:
        if args.format == "json":
            print(format_as_json(results))
        else:
            print(format_as_markdown(results))
    else:
        print("No issues found.")

if __name__ == "__main__":
    main()
