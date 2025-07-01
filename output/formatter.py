# output/formatter.py
import json

def format_as_json(results):
    return json.dumps(results, indent=2)

def format_as_markdown(results):
    md = "# Lintinel Report\n\n"

    for rule_result in results:
        md += f"## {rule_result['name']}\n"
        md += f"{rule_result['description']}\n\n"

        issues = rule_result.get("issues", [])

        if not issues:
            md += "- ✅ No issues found.\n"
            continue

        for idx, issue in enumerate(issues, 1):
            if isinstance(issue, str):
                md += f"- {issue}\n"
            elif isinstance(issue, dict):
                md += f"### Issue {idx}\n"

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
                    md += f"\n{ai_fix.strip()}\n\n"

    return md
