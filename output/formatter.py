# output/formatter.py
import json


def format_as_json(results):
    return json.dumps(results, indent=2)


def format_as_markdown(results):
    md = "# Lintinel Report\n\n"

    for rule_result in results:
        issues = rule_result.get("issues", [])

        # Skip rules with only success messages
        if all(isinstance(issue, dict) and issue.get("message", "").startswith("✅") for issue in issues):
            continue

        md += f"## {rule_result['name']}\n"
        md += f"{rule_result['description']}\n\n"

        issue_counter = 1
        for issue in issues:
            # Skip individual "✅" messages too, just in case
            if isinstance(issue, dict) and issue.get("message", "").startswith("✅"):
                continue

            md += f"### Issue {issue_counter}\n"

            if isinstance(issue, str):
                md += f"- {issue}\n"
            elif isinstance(issue, dict):
                file = issue.get("file", "Unknown file")
                line = issue.get("line", "N/A")
                message = issue.get("message", "")
                code = issue.get("code", "")
                ai_fix = issue.get("ai_fix", "")

                md += f"- **File**: `{file}` — Line {line}\n"
                md += f"  - **Issue**: {message}\n"
                if code:
                    md += f"  - **Code**:\n```yaml\n{code.strip()}\n```\n"
                if ai_fix:
                    md += f"\n\n{ai_fix.strip()}\n\n"

            issue_counter += 1
        md += "\n"

    return md
