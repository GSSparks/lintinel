#!/bin/env python
# main.py

import os
import importlib
import yaml
from dotenv import load_dotenv
from rules.base import Rule
from output.formatter import format_as_json, format_as_markdown
from utils.repo_loader import prepare_repo
from utils.git_diff import get_changed_files
from ai.summarizer import generate_summary
from ai.fixer import suggest_fix

load_dotenv()  # Load OPENAI_API_KEY from .env

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
                if (
                    isinstance(obj, type) and
                    issubclass(obj, Rule) and
                    obj != Rule
                ):
                    rules.append(obj())
    return rules


def run_lint(repo_url, branch=None, token=None, output_format="json"):
    try:
        repo_path = prepare_repo(repo_url, token=token, branch=branch)
    except Exception as e:
        return f"Error preparing repository: {e}"

    rules = load_rules()
    results = []
    config = load_config(repo_path)
    enabled_rules = config.get("rules", {}) if config else {}
    ai_config = config.get("ai", {})
    git_config = config.get("git", {})

    summary = None
    fixed_locations = set()
    changed_files = set()

    if git_config.get("pr_diff_only"):
        try:
            base_ref = git_config.get("base_ref", "origin/main")
            changed_files = get_changed_files(repo_path, base_ref)
        except Exception as e:
            print(f"Warning: Failed to get PR diff: {e}")

    for rule in rules:
        rule_name = rule.__class__.__name__
        if enabled_rules and not enabled_rules.get(rule_name, True):
            continue

        try:
            result = rule.run(repo_path, changed_files=changed_files if changed_files else None)
            if result:
                if ai_config.get("fixes"):
                    for issue in result.get("issues", []):
                        file_path = issue.get("file")
                        line_no = issue.get("line")
                        code_sample = issue.get("code", "")
                        location_key = f"{file_path}:{line_no}"

                        if file_path and isinstance(line_no, int):
                            if any(
                                abs(line_no - int(loc.split(":")[1])) <= 1
                                for loc in fixed_locations
                                if loc.startswith(file_path)

                            ):
                                continue
                            full_path = os.path.join(repo_path, file_path)
                            if os.path.exists(full_path):
                                try:
                                    with open(full_path, "r") as f:
                                        lines = f.readlines()
                                    start = max(0, line_no - 4)
                                    end = min(len(lines), line_no + 3)
                                    context_snippet = (
                                        "".join(lines[start:end])
                                        .strip()
                                    )
                                except Exception:
                                    context_snippet = (
                                        code_sample or "[Could not read surrounding lines]"
                                    )
                            else:
                                context_snippet = (
                                    code_sample or "[File not found]"
                                )
                        else:
                            context_snippet = code_sample

                        if context_snippet:
                            fix = suggest_fix(
                                file_path=file_path or "unknown file",
                                code=context_snippet,
                                rule_name=rule_name,
                                issue=issue.get("message", "Unspecified issue"),
                                tone=ai_config.get("tone", "helpful")
                            )
                            issue["ai_fix"] = fix
                            fixed_locations.add(location_key)

                results.append(result)

        except Exception as e:
            results.append({
                "name": rule.name,
                "description": rule.description,
                "issues": [f"Error running rule: {e}"]
            })

    if ai_config.get("enabled") and results:
        tone = ai_config.get("tone", "helpful")
        summary = generate_summary(results, tone=tone)

    if output_format == "json":
        output_data = {
            "results": results,
        }
        if summary:
            output_data["ai_summary"] = summary
        return format_as_json(output_data)

    elif output_format == "markdown":
        md = format_as_markdown(results)
        if summary:
            md += "\n\n## Summary\n\n" + summary
        return md

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
